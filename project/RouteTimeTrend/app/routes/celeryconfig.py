__author__ = 'vchang'

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'ten-minutes': {
        'task': 'app.routes.tasks.trigger_grab',
        'schedule': crontab(minute='*/10'),
        'args': (2),
    },
}