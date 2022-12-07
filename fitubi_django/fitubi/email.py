from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_to_fitubi(user, title, message):
    email_to = 'fitubi.staff@gmail.com'
    context = {
        'title': title,
        'message': message,
        'user': user
    }

    email_subject = f'User {user}: {title}'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(email_subject, email_body,
                         settings.DEFAULT_FROM_EMAIL, [email_to, ],
                         )
    return email.send(fail_silently=False)
