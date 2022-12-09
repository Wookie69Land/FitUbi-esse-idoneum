from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitubi_django.settings')

app = Celery('fitubi_django')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

