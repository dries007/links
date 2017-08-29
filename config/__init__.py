import os

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@localhost/%s' % (os.environ['POSTGRES_USER'], os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_DB'])
SECRET_KEY = os.environ['FLASK_SECRET']

TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

STATIC_FOLDER = './static'

TOKEN_LENGTH = 25
LINK_LENGTH = 10
