from sqlalchemy import create_engine
import psycopg2
from os import getenv

user = getenv('AMANIGO_USER')
password = getenv('AMANIGO_PWD')
database = getenv('AMANIGO_DB')
host = getenv('AMANIGO_HOST')


SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
ADMIN_EMAIL = "admin@personal.com"
USER_PROFILE_PATH = "amanigo/static/images/"
POST_IMAGE_PATH = "amanigo/static/images/post/"
DEST_IMAGE_PATH = "amanigo/static/images/destinations/"
PACKAGE_IMAGE_PATH = "amanigo/static/images/packages/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
SPECIAL_OFFER_IMAGE_PATH = "amanigo/static/images/specialoffers/"
SQLALCHEMY_DATABASE_URI=f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"


MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USERNAME='carryoby@gmail.com'
MAIL_PASSWORD='pzvw jfdf swwa lmcw'
MAIL_USE_SSL=True
