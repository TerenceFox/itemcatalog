import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SERVER_NAME = 'catalog.terencefox.me'
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Global variable for OAuth
    CLIENT_SECRET_FILE =  os.path.join(basedir, 'client_secret.json')
    CLIENT_ID = json.loads(
        open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']
