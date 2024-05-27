from sqlalchemy import create_engine

import mysql.connector

config = {
    'user': 'root',
    'password':'',
    'host': '127.0.0.1',
    'database': 'amanigotravels',
    'charset': 'utf8mb4'
}
connection = mysql.connector.connect(**config)

SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
ADMIN_EMAIL="admin@personal.com"
USER_PROFILE_PATH="amanigo/static/images/"
POST_IMAGE_PATH = "amanigo/static/images/post/"
DEST_IMAGE_PATH = "amanigo/static/images/destinations/"
PACKAGE_IMAGE_PATH = "amanigo/static/images/packages/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
SPECIAL_OFFER_IMAGE_PATH ="amanigo/static/images/specialoffers/"
SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/amanigotravels?charset=utf8mb4"
engine = create_engine('mysql+mysqlconnector://root@localhost/amanigotravels?charset=utf8mb4', echo=True)


MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USERNAME='carryoby@gmail.com'
MAIL_PASSWORD='uxjq wcqv yntk dwju'
MAIL_USE_SSL=True