DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://routetimeuser:passw0rd@traffic-db/routetime'
    DATABASE_CONNECT_OPTIONS = {}

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSRF_ENABLED = True

    CSRF_SESSION_KEY = 'putsomethinghere'
    SECRET_KEY = 'put something here'
