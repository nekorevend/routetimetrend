
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'psql:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True

CSRF_SESSION_KEY = 'putsomethinghere'
SECRET_KEY = 'put something here'