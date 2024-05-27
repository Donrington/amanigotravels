from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, PasswordField, SubmitField,FloatField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed, FileRequired


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = TextAreaField('Subtitle', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    categories = SelectField('Categories', choices=[
        ('Adventure Travel', 'Adventure Travel'),
        ('Business Travel', 'Business Travel'),
        ('Family Vacations', 'Family Vacations'),
        ('Honeymoon and Romance', 'Honeymoon and Romance'),
        ('Budget Travel', 'Budget Travel'),
        ('Luxury Travel', 'Luxury Travel'),
        ('Ecotourism', 'Ecotourism'),
        ('Cultural and Historical Tours', 'Cultural and Historical Tours'),
        ('Cruises', 'Cruises'),
        ('Beach Holidays', 'Beach Holidays'),
        ('Wellness and Health', 'Wellness and Health'),
        ('Festival and Events', 'Festival and Events'),
        ('Food and Wine Tours', 'Food and Wine Tours'),
        ('Sports Travel', 'Sports Travel'),
        ('Religious Tours', 'Religious Tours'),
        ('Hajj and Umrah', 'Hajj and Umrah'),
        ('Educational Travel', 'Educational Travel')
    ])
    tags = StringField('Tags') # Allowing multiple tags, consider using a field that supports multiple selections


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Sign In')

class OTPSendForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send OTP')

class OTPForm(FlaskForm):
    otp_code = StringField('OTP Code', validators=[DataRequired()])
    submit = SubmitField('Verify OTP')

class DestinationForm(FlaskForm):
    name = StringField('Destination Name', validators=[DataRequired()])
    subtitle = TextAreaField('Subtitle', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Create Destination')


class SpecialOfferForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = TextAreaField('Subtitle', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Create Special Offer')


class PackageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    amount = FloatField('Amount (₦)', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
