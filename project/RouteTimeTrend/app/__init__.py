__author__ = 'vchang'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.routes.controllers import routes
app.register_blueprint(routes)

db.create_all()
