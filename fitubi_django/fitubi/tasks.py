from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model

from celery import shared_task
from celery.utils.log import get_task_logger

from .email import send_to_fitubi
from .models import UserActivatedPlan


logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task(name='send_message_to_fitubi')
def send_message_to_fitubi_task(user, title, message):
    logger.info("Send message to FitUbi")
    return send_to_fitubi(user, title, message)


@shared_task
def send_mail_to_all_users(self):
    users = get_user_model().objects.all()
    for user in users:
        pass
    logger.info("Email to all users send")
    return "Done"


@shared_task
def send_mail_activated_plan(self):
    users = get_user_model().objects.all()
    for user in users:
        if UserActivatedPlan.objects.filter(user=user).exists():
            pass
    logger.info("Email to users with activated plan send")
    return "Done"

