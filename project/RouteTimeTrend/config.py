DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://routetimeuser:passw0rd@localhost/routetime'
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True

CSRF_SESSION_KEY = 'putsomethinghere'
SECRET_KEY = 'put something here'