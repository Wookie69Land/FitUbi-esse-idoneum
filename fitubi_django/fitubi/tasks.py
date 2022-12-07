from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from .email import send_to_fitubi


logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task(name='send_message_to_fitubi')
def send_message_to_fitubi_task(user, title, message):
    logger.info("Send message to FitUbi")
    return send_to_fitubi(user, title, message)

