from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User

from celery import shared_task
from celery.utils.log import get_task_logger

from fitubi.email import send_to_fitubi, send_to_all, send_to_users_activated_plan
from fitubi.models import UserActivatedPlan


logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task(name='send_message_to_fitubi')
def send_message_to_fitubi_task(user, title, message):
    logger.info("Send message to FitUbi")
    return send_to_fitubi(user, title, message)


@shared_task(name='send_monday_email_to_all_task')
def send_monday_email_to_all_task():
    users = User.objects.all()
    title = "Wish you best week"
    message = "We want to wish you best possible week on our journey to healthy and fulfilled life. " \
              "Take care of yourself!"
    logger.info("Trying to send email to all users!")
    return send_to_all(users, title, message)


@shared_task(name='send_email_activated_plan_task')
def send_email_activated_plan_task():
    active_plans = UserActivatedPlan.objects.all()
    users = User.objects.filter(useractivatedplan__in=active_plans)
    logger.info("Email to users with activated plan send")
    return send_to_users_activated_plan(users)

