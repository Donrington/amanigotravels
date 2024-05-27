from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_mail import Mail,Message
csrf = CSRFProtect()


mail = Mail()
def create_app():
    from amanigo.models import db
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile("config.py", silent=True)
    app.config['JSON_AS_ASCII'] = False
    db.init_app(app)
    migrate = Migrate(app,db)
    socketio = SocketIO(app)
    csrf.init_app(app)
    mail.init_app(app)
    Bootstrap(app) 
    return app, socketio
app, socketio = create_app()


from amanigo import user_routes, admin_routes
from amanigo.forms import *