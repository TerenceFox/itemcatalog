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
from app import routes, models
