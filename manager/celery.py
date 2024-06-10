# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

app = Celery('manager')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-reservations-every-30-minutes': {
        'task': 'seats.tasks.delete_expired_reservations',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}
