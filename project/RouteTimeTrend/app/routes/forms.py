__author__ = 'vchang'
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class AddRouteForm(Form):
    name = StringField('Route Name', [DataRequired(message='Must give the route a name')])
    url = StringField('Google Maps permalink', [DataRequired(message='Must give a route URL')])
