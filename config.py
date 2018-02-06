import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Global variable for OAuth
    CLIENT_SECRET_FILE = 'app/client_secret.json'
    CLIENT_ID = json.loads(
        open('app/client_secret.json', 'r').read())['web']['client_id']
