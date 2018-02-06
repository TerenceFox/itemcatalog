from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

#Initialization of Flask
app = Flask(__name__)
#Set global variables
app.config.from_object(Config)
#Initialize database
db = SQLAlchemy(app)

#Initialize database models and routing
from app import models
from .routes import api
from .routes import index
from .routes import gconnect
from .routes import gdisconnect
from .routes import createcategory
from .routes import editcategory
from .routes import deletecategory
from .routes import category
from .routes import createitem
from .routes import edititem
from .routes import deleteitem
