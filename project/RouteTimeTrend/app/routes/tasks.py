__author__ = 'vchang'

from celery import Celery

from app.routes.controllers import manual_route_poll

celery = Celery('tasks')
celery.config_from_object('app.routes.celeryconfig')

@celery.task
def trigger_grab(route_id):
    save_duration(route_id)