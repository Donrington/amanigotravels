
from sqlalchemy import create_engine
import psycopg2

config = {
    'user': 'amanigotravels_znjz_user',
    'password': 'Ew0KClpMdEFm3uWK7JAGPHQIH1aE0eLq',
    'host': 'dpg-cqa6uv3v2p9s73cs4520-a.oregon-postgres.render.com',
    'database': 'amanigotravels_znjz'
}

# Connect to PostgreSQL using psycopg2
connection = psycopg2.connect(
    user=config['user'],
    password=config['password'],
    host=config['host'],
    database=config['database']
)

SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
ADMIN_EMAIL = "admin@personal.com"
USER_PROFILE_PATH = "amanigo/static/images/"
POST_IMAGE_PATH = "amanigo/static/images/post/"
DEST_IMAGE_PATH = "amanigo/static/images/destinations/"
PACKAGE_IMAGE_PATH = "amanigo/static/images/packages/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
SPECIAL_OFFER_IMAGE_PATH = "amanigo/static/images/specialoffers/"
SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/amanigotravel"

# SQLAlchemy database URI for PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://amanigotravels_znjz_user:Ew0KClpMdEFm3uWK7JAGPHQIH1aE0eLq@dpg-cqa6uv3v2p9s73cs4520-a.oregon-postgres.render.com/amanigotravels_znjz"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'carryoby@gmail.com'
MAIL_PASSWORD = 'pzvw jfdf swwa lmcw'
MAIL_USE_SSL = True