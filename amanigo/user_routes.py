from PIL import Image
import json, os
import io
from os.path import basename
import random
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from flask import * 
from flask_socketio import SocketIO, emit, join_room, leave_room
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect, generate_csrf
from amanigo import *
from amanigo.forms import *
from amanigo.models import *
from flask_login import login_required
from amanigo.models import db
from sqlalchemy import func,desc  
from datetime import datetime, timedelta
import pytz


socketio = SocketIO(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('user/404.html', pagename='Page Not Found | Amanigo Travels'), 404

# Your existing log
# in_required decorator
def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if session.get("logged_in") is not None:
            return f(*args, **kwargs)
        else:
            flash("Access Denied")
            return redirect(url_for('login'))
    return login_check


# Example of applying the decorator@app.route('/admin_dashboard')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        flash('You need to login to access the admin dashboard')
        return redirect(url_for('login'))
    # Retrieve the logged-in user's information if needed
    user = User.query.filter_by(username=session.get('username')).first()
    posts = Post.query.options(db.joinedload(Post.categories)).all()
  # Fetch all posts for display
    return render_template('user/admindashboard.html', pagename='Admin Dashboard | Amanigo Travels', user=user, posts=posts)

@app.route('/logout')
def logout():
    session.clear()  # Clears all data from session
    flash('You have been logged out.')
    return redirect(url_for('login'))





def generate_otp():
    return str(random.randint(100000, 999999))  # Generate OTP as a string


def send_otp():
    form = OTPSendForm()
    if form.validate_on_submit():
        email = form.email.data
        otp = str(generate_otp())
        timezone = pytz.timezone("Europe/London")  # Replace "Your/Timezone" with your time zone, e.g., "Asia/Kolkata"
        expiration = datetime.now(timezone) + timedelta(minutes=10)
        session['otp'] = otp
        session['otp_email'] = email
        session['otp_expiration'] = expiration.isoformat()
        flash(f'OTP sent to your email: {otp}')  # Debugging purpose
        return render_template('verify_otp.html', form=form)
    return render_template('user/send_otp.html', form=form)


@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user_otp = form.otp_code.data

        if user and user.otp == user_otp:
            # Clear the OTP after successful verification
            user.otp = None
            db.session.commit()

            # Set session to logged-in state
            session['logged_in'] = True
            session['username'] = user.username

            flash('OTP verified successfully!')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect OTP.')

    return render_template('user/verify_otp.html', form=form)

    
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Generate OTP and store it
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.otp = otp
            db.session.commit()

            # Send OTP via email
            msg = Message("Your Admin Login OTP", sender=app.config['MAIL_USERNAME'], recipients=[user.email])
            msg.body = f"Your OTP is {otp}."
            mail.send(msg)

            # Save user id in session for further verification in verify_otp
            session['user_id'] = user.id
            flash('OTP has been sent to your email.')
            return redirect(url_for('verify_otp'))
        else:
            flash('Invalid username or password')
    return render_template('user/login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)  # Default to False for admin
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('user/registration.html', form=form, pagename='Admin Registration | Amanigo Travels')



@app.route('/')
def index():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    posts = Post.query.order_by(Post.post_date.desc()).limit(3).all()  # Fetch the latest three posts
    destinations = Destination.query.limit(4).all()  # Fetch the latest four destinations
    special_offers = SpecialOffer.query.order_by(SpecialOffer.offer_date.desc()).limit(3).all()
    packages = Package.query.order_by(Package.id.desc()).limit(3).all()
    return render_template('user/index.html', pagename='Homepage | Amanigo Travels', posts=posts, user=user, destinations=destinations, special_offers=special_offers, packages=packages)

    

@app.route("/blog/<int:post_id>")
def blog(post_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    destinations = Destination.query.all() 
    if post:
        return render_template("user/blog.html", post=post, destinations=destinations, user=user, pagename='Blog | Amanigo Travels')
    else:
        flash("Post not found", "error")
        return render_template("user/blog.html", pagename='Blog | Amanigo Travels')


@app.route("/bloglist/")
def bloglist():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    categories = Category.query.order_by(Category.name).all()  # Fetch all categories
    posts = Post.query.order_by(Post.post_date.desc()).all()  # Fetch all posts
    return render_template("user/blog-list.html", pagename='Blog List | Amanigo Travels', categories=categories, posts=posts, user=user)


@app.route('/fetch_posts_by_category/<int:category_id>')
def fetch_posts_by_category(category_id):
    posts = Post.query.join(post_category).filter(post_category.c.category_id == category_id).order_by(Post.post_date.desc()).all()

    posts_data = [
        {
            'id': post.id,
            'title': post.title,
            'image': post.image,
            'post_date': post.post_date.strftime('%B %d, %Y')
        }
        for post in posts
    ]

    return jsonify({'posts': posts_data})



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image, save_path):
    if image and allowed_file(image.filename):
        try:
            filename = secure_filename(image.filename)
            image_path = os.path.join(save_path, filename)

            # Save original image
            image.save(image_path)
            print(f"Image saved to path: {image_path}")  # Debug statement

            return filename
        except Exception as e:
            print(f"Failed to save image: {e}")  # Debug statement
            return None
    return None
@app.route("/user/new_post", methods=['GET', 'POST'])
def new_post():
    if 'logged_in' not in session or not session['logged_in']:
        flash('You need to log in to create a new post.', 'error')
        return redirect(url_for('login'))

    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data
        image = request.files['image'] if 'image' in request.files else None
        image_url = form.image_url.data.strip() if form.image_url.data else None

        # Ensure only one is used
        if image and image_url:
            flash('Please provide either an image file or an image URL, not both.', 'error')
            return render_template("user/new_post.html", form=form)

        # Save the image file or use the URL
        if image:
            image_filename = save_image(image, app.config['POST_IMAGE_PATH'])
            final_image_url = os.path.join('/static/images/post/', image_filename)
        else:
            final_image_url = image_url

        user_id = session.get('user_id')
        new_post = Post(title=title, subtitle=subtitle, content=content, image=final_image_url, author_id=user_id)

        selected_category_names = form.categories.data.split(',')
        for category_name in selected_category_names:
            category = Category.query.filter_by(name=category_name.strip()).first()
            if not category:
                category = Category(name=category_name.strip())
                db.session.add(category)
            new_post.categories.append(category)

        selected_tag_names = form.tags.data.split(',')
        for tag_name in selected_tag_names:
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.session.add(tag)
            new_post.tags.append(tag)

        db.session.add(new_post)
        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template("user/new_post.html", form=form)
@app.route("/create_destination", methods=['GET', 'POST'])
def create_destination():
    if 'logged_in' not in session or not session['logged_in']:
        flash('You need to log in to create a destination.', 'error')
        return redirect(url_for('login'))
    
    form = DestinationForm()
    if form.validate_on_submit():
        name = form.name.data
        subtitle = form.subtitle.data
        description = form.description.data
        image = request.files['image'] if 'image' in request.files else None
        image_url = form.image_url.data.strip() if form.image_url.data else None

        # Ensure that only one image source is provided
        if image and image_url:
            flash('Please provide either an image file or an image URL, not both.', 'error')
            return render_template('user/create_destination.html', form=form)

        # Handle the image upload or use the URL
        if image:
            image_filename = save_image(image, app.config['DEST_IMAGE_PATH'])
            final_image_url = os.path.join('/static/images/post/', image_filename)
        else:
            final_image_url = image_url

        user_id = session.get('user_id')
        new_destination = Destination(name=name, subtitle=subtitle, description=description, author_id=user_id)
        db.session.add(new_destination)
        db.session.commit()

        new_image = Image(url=final_image_url, destination_id=new_destination.id)
        db.session.add(new_image)
        db.session.commit()

        flash('Destination created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('user/create_destination.html', form=form)


@app.route("/destination/<int:destination_id>")
def view_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    posts = Post.query.order_by(Post.post_date.desc()).all()  # Fetch all posts
    return render_template("user/destinations.html", pagename='Destination | Amanigo Travels', destination=destination, user=user, posts=posts)



@app.route("/destinationlist/")
def destination_list():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    destinations = Destination.query.all()  # Fetch all destinations
    return render_template("user/destination-list.html",pagename ='Destination List | Amanigo Travels', user=user, destinations=destinations)


@app.route("/special-offer/<int:offer_id>")
def view_special_offer(offer_id):
    special_offer = SpecialOffer.query.get_or_404(offer_id)
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    destinations = Destination.query.all() 
    return render_template("user/special-offer.html", special_offer=special_offer, user=user, pagename ='Special Offers | Amanigo Travels', destinations=destinations)

@app.route("/special-offers/")
def special_offers_list():
    special_offers = SpecialOffer.query.order_by(SpecialOffer.offer_date.desc()).all()
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return render_template("user/special-offers-list.html", special_offers=special_offers, user=user, pagename ='Special Offers | Amanigo Travels')
@app.route("/special-offer/new", methods=['GET', 'POST'])
def new_special_offer():
    if 'user_id' not in session or not session['user_id']:
        flash('You need to log in to create a new special offer.', 'error')
        return redirect(url_for('login'))
    
    form = SpecialOfferForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data
        image = request.files['image'] if 'image' in request.files else None
        image_url = form.image_url.data.strip() if form.image_url.data else None

        # Ensure that only one image source is provided
        if image and image_url:
            flash('Please provide either an image file or an image URL, not both.', 'error')
            return render_template('user/specialofferpost.html', form=form)

        # Handle the image upload or use the URL
        if image:
            image_filename = save_image(image, app.config['SPECIAL_OFFER_IMAGE_PATH'])
            final_image_url = os.path.join('/static/images/special_offers/', image_filename)
        else:
            final_image_url = image_url

        user_id = session.get('user_id')
        new_special_offer = SpecialOffer(
            title=title, 
            subtitle=subtitle, 
            content=content, 
            image=final_image_url, 
            author_id=user_id
        )
        db.session.add(new_special_offer)
        db.session.commit()

        flash('Special Offer created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('user/specialofferpost.html', form=form)


@app.route("/packages/<int:package_id>")
def view_package(package_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    package = Package.query.get_or_404(package_id)
    special_offers = SpecialOffer.query.order_by(SpecialOffer.offer_date.desc()).limit(3).all()
    return render_template("user/packages.html", package=package, user=user, special_offers=special_offers)

@app.route("/packages")
def packages_list():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    packages = Package.query.all()
    return render_template("user/packages-list.html", packages=packages, user=user)


import logging
# Configure logging
logging.basicConfig(level=logging.DEBUG)
@app.route("/create_package", methods=['GET', 'POST'])
def create_package():
    form = PackageForm()
    if form.validate_on_submit():
        try:
            title = form.title.data
            subtitle = form.subtitle.data
            amount = form.amount.data
            content = form.content.data
            image = request.files['image'] if 'image' in request.files else None
            image_url = form.image_url.data.strip() if form.image_url.data else None
            
            # Ensure that only one image source is provided
            if image and image_url:
                flash('Please provide either an image file or an image URL, not both.', 'error')
                return render_template('user/packagespost.html', form=form)

            # Handle the image upload or use the URL
            if image:
                image_filename = save_image(image, app.config['PACKAGE_IMAGE_PATH'])
                final_image_url = os.path.join('/static/images/packages/', image_filename)
            else:
                final_image_url = image_url

            user_id = session.get('user_id')

            if not user_id:
                flash('User not logged in.', 'error')
                return redirect(url_for('login'))

            new_package = Package(
                title=title,
                subtitle=subtitle,
                amount=amount,
                content=content,
                image=final_image_url,
                author_id=user_id
            )
            db.session.add(new_package)
            db.session.commit()

            flash('Package created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            logging.error("Error creating package: %s", str(e))
            flash(f'An error occurred: {str(e)}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                logging.error("Error in %s: %s", getattr(form, field).label.text, error)
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')

    return render_template('user/packagespost.html', form=form)


@app.route('/visa', methods=['GET', 'POST'])
@csrf.exempt
def visa():
    if request.method == 'POST':
        try:
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            dob = request.form['dob']
            country = request.form['country']
            email = request.form['email']
            phone = request.form['phone']

            # Debugging: Print received form data
            logging.debug(f"Received form data: first_name={first_name}, last_name={last_name}, dob={dob}, country={country}, email={email}, phone={phone}")

            # Convert dob to datetime object
            dob = datetime.strptime(dob, '%Y-%m-%d')

            new_application = VisaApplication(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                country=country,
                email=email,
                phone=phone
            )

            db.session.add(new_application)
            db.session.commit()

            flash('Visa application   submitted successfully!', 'success')
            return redirect(url_for('visa'))
        except Exception as e:
            # Debugging: Print the exception
            logging.error(f"Error submitting visa application: {e}")
            db.session.rollback()
            flash('Error submitting visa application. Please try again.', 'danger')

    return render_template('user/visapage.html')


@app.route('/visa_applications', methods=['GET'])
@csrf.exempt
def visainfo():
    user_id = session.get('user_id')  # Retrieve the user ID from the session
    if not user_id:
        flash('You need to log in to view visa applications.', 'error')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    query = request.args.get('query')
    if query:
        applications = VisaApplication.query.filter(
            (VisaApplication.first_name.ilike(f'%{query}%')) |
            (VisaApplication.last_name.ilike(f'%{query}%')) |
            (VisaApplication.country.ilike(f'%{query}%')) |
            (VisaApplication.email.ilike(f'%{query}%')) |
            (VisaApplication.phone.ilike(f'%{query}%'))
        ).all()
    else:
        applications = VisaApplication.query.all()
    return render_template('user/visainfo.html', pagename='Visa Applications | Amanigo Travels', applications=applications, query=query, user=user)

@app.route('/delete_visa_application/<int:application_id>', methods=['POST'])
@csrf.exempt
def delete_visa_application(application_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to perform this action.', 'error')
        return redirect(url_for('login'))

    application = VisaApplication.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    flash('Visa application deleted successfully!', 'success')
    return redirect(url_for('visainfo'))

@app.route('/homecontent')
def homecontent():
    if not session.get('user_id'):
        flash('You need to login to access the admin dashboard')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=session.get('username')).first()
    posts = Post.query.options(db.joinedload(Post.categories)).all()
    packages = Package.query.all()
    destinations = Destination.query.all()
    offers = SpecialOffer.query.all()
    
    return render_template('user/homecontent.html', pagename='Homepage Content | Amanigo Travels', user=user, posts=posts, packages=packages, destinations=destinations, offers=offers)


@app.route('/api/dashboard-data')
def dashboard_data():
    new_package = Package.query.count()
    new_destination = Destination.query.count()
    new_posts = Post.query.count()
    new_visa_applications = VisaApplication.query.count()
    new_special_offers = SpecialOffer.query.count()
    new_contacts = Contact.query.count()
    new_newsletter_subscribers = Newsletter.query.count()

    data = {
        'new_package': new_package,
        'new_destination': new_destination,
        'new_posts': new_posts,
        'new_visa_applications': new_visa_applications,
        'new_special_offers': new_special_offers,
        'new_contacts': new_contacts,
        'new_newsletter_subscribers': new_newsletter_subscribers
    }
    return jsonify(data)



@app.route('/api/visa-applications-data')
def visa_applications_data():
    current_year = datetime.now().year
    date_format = f'%Y-%m'

    visa_applications = db.session.query(
        func.DATE_FORMAT(VisaApplication.created_at, date_format).label('month'),
        func.count(VisaApplication.id).label('count')
    ).group_by('month').order_by('month').all()

    labels = [app.month for app in visa_applications]
    data = [app.count for app in visa_applications]

    applications_over_time = {
        'labels': labels,
        'data': data
    }
    return jsonify(applications_over_time)


@app.route("/help-center/")
def helpcenter():
    return render_template("user/help-center.html", pagename = 'Help Center | Amanigo Travels')

@app.route("/contact/")
def contact():
    return render_template("user/contact.html", pagename = 'Contact Us | Amanigo Travels')


@app.route("/submit_contact", methods=['POST'])
@csrf.exempt
def submit_contact():
    try:
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        new_contact = Contact(
            contact_name=full_name,
            contact_email=email,
            contact_subject=subject,
            contact_message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while sending your message. Please try again.', 'danger')
        return redirect(url_for('contact'))
    
@app.route('/contactinfo/')
@csrf.exempt
def contact_data():
    query = request.args.get('query')
    if query:
        contacts = Contact.query.filter(
            (Contact.contact_name.like(f'%{query}%')) |
            (Contact.contact_email.like(f'%{query}%')) |
            (Contact.contact_subject.like(f'%{query}%')) |
            (Contact.contact_message.like(f'%{query}%'))
        ).all()
    else:
        contacts = Contact.query.all()
    return render_template('user/contactinfo.html', pagename='Contact Information | Amanigo Travels', contacts=contacts, query=query)

@app.route('/delete_contact/<int:contact_id>', methods=['POST'])
@csrf.exempt
def delete_contact(contact_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to perform this action.', 'error')
        return redirect(url_for('login'))

    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact message deleted successfully!', 'success')
    return redirect(url_for('contact_data'))

@app.route("/core_services/")
def core_services():
    return render_template("user/core_services.html", pagename='Core Services | Amanigo Travels')

@app.route("/terms/")
def terms():
    return render_template("user/terms.html", pagename = 'Terms | Amanigo Travels')


@app.route('/submit_newsletter', methods=['POST'])
@csrf.exempt
def submit_newsletter():
    try:
        email = request.form.get('email')
        new_subscriber = Newsletter(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        flash('You have successfully subscribed to the newsletter!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while subscribing. Please try again.', 'danger')
    return redirect(url_for('index'))


@app.route("/about/")
def about():
    return render_template("user/about.html", pagename = 'About | Amanigo Travels')


@app.route('/newsletter_subscribers')
def view_newsletter_subscribers():
    subscribers = Newsletter.query.all()
    return render_template('user/newsletter_subscribers.html', subscribers=subscribers)

@app.route('/delete_subscriber/<int:subscriber_id>', methods=['POST'])
@csrf.exempt
def delete_subscriber(subscriber_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to perform this action.', 'error')
        return redirect(url_for('login'))

    subscriber = Newsletter.query.get_or_404(subscriber_id)
    db.session.delete(subscriber)
    db.session.commit()
    flash('Subscriber deleted successfully!', 'success')
    return redirect(url_for('view_newsletter_subscribers'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@csrf.exempt
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('homecontent'))

@app.route('/delete_package/<int:package_id>', methods=['POST'])
@csrf.exempt
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('homecontent'))

@app.route('/delete_destination/<int:destination_id>', methods=['POST'])
@csrf.exempt
def delete_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    db.session.delete(destination)
    db.session.commit()
    flash('Destination deleted successfully!', 'success')
    return redirect(url_for('homecontent'))

@app.route('/delete_offer/<int:offer_id>', methods=['POST'])
@csrf.exempt
def delete_offer(offer_id):
    offer = SpecialOffer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    flash('Special Offer deleted successfully!', 'success')
    return redirect(url_for('homecontent'))
@app.route('/change_credentials', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access this
@csrf.exempt
def change_credentials():
    user = User.query.filter_by(username=session.get('username')).first()
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        new_email = request.form.get('new_email')

        if not user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
        elif new_password and new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        else:
            if new_password:
                user.set_password(new_password)
            if new_email and new_email != user.email:
                user.email = new_email
            db.session.commit()
            flash('Credentials updated successfully.', 'success')
            return redirect(url_for('change_credentials'))

    return render_template('user/change_credentials.html', user=user)
