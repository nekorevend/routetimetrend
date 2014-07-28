__author__ = 'vchang'

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')

from app.routes.controllers import routes
app.register_blueprint(routes)

db.create_all()