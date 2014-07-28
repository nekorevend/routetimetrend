__author__ = 'vchang'

from app import db


class RouteTime(db.Model):
    __tablename__ = 'route_time'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    duration = db.Column(db.Interval)
    timestamp = db.Column(db.DateTime)

    route = db.relationship('Route', backref=db.backref('route_times'))


class Route(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
