
from sqlalchemy import create_engine
import psycopg2

config = {
    'user': 'amanigotravels_user',
    'password': '9uQcR5JtxHxLQIMHd1OTxZ8V800HwdcT',
    'host': 'dpg-cpafck4f7o1s73ag5350-a.oregon-postgres.render.com',
    'database': 'amanigotravels'
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

# SQLAlchemy database URI for PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://amanigotravels_user:9uQcR5JtxHxLQIMHd1OTxZ8V800HwdcT@dpg-cpafck4f7o1s73ag5350-a.oregon-postgres.render.com/amanigotravels"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'carryoby@gmail.com'
MAIL_PASSWORD = 'uxjq wcqv yntk dwju'
MAIL_USE_SSL = True