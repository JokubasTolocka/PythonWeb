from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('loging.log', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
root_logger.addHandler(handler)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import views, models