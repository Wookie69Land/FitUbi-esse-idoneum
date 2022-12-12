from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitubi_django.settings')

app = Celery('fitubi_django')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_monday_email_to_all_task': {
        'task': 'send_monday_email_to_all_task',
        'schedule': crontab(day_of_week=1, hour=7, minute=30),
    },
    'send_email_activated_plan_task': {
        'task': 'send_email_activated_plan_task',
        'schedule': crontab(day_of_week=6, hour=16, minute=0),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

