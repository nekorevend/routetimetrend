__author__ = 'vchang'

from app import db


class RouteTime(db.IdModel):
    __tablename__ = 'route_time'

    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    duration = db.Column(db.Interval)

    route = db.relationship('Route', backref=db.backref('route'))


class Route(db.IdModel):
    __tablename__ = 'route'

    url = db.Column(db.String)
