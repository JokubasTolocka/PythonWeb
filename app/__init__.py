from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
logging.basicConfig(filename='loging.log', encoding='utf-8', level=logging.DEBUG)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import views, models