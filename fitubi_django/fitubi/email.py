#functions for sending emails used by celery
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import UserActivatedPlan, RecipePlan
from .fitubi_utils import process_plan_week


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


def send_to_all(users, title, message):
    for user in users:
        context = {
            'title': title,
            'message': message,
            'user': user.username
        }

        email_subject = f'User {user}: {title}'
        email_body = render_to_string('email_to_all.txt', context)

        email = EmailMessage(email_subject, email_body,
                             settings.DEFAULT_FROM_EMAIL, [user.email, ],
                             )
        email.send(fail_silently=True)
    return "Emails sent"


def send_to_users_activated_plan(users):
    for user in users:
        activated_plan = get_object_or_404(UserActivatedPlan, user=user)
        plan = activated_plan.plan
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)

        title = f'Activated plan: {plan} for next week for {user}'
        message = 'You will need this ingredients for your recipes: \n'
        message += f'Monday:\n'
        for dish in monday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'
        message += f'Tuesday:\n'
        for dish in tuesday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'
        message += f'Wednesday:\n'
        for dish in wednesday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'
        message += f'Thursday:\n'
        for dish in thursday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'
        message += f'Friday:\n'
        for dish in friday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'
        message += f'Saturday:\n'
        for dish in saturday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'
        message += f'Sunday:\n'
        for dish in sunday:
            message += f'{dish.recipe}:\n'
            for row in dish.recipe.recipeingredients_set.all():
                message += f'{row.ingredient} - {row.amount}{row.ingredient.unit}\n'

        context = {
            'title': title,
            'message': message,
            'user': user.username
        }

        email_subject = f'User {user}: {title}'
        email_body = render_to_string('email_to_all.txt', context)

        email = EmailMessage(email_subject, email_body,
                             settings.DEFAULT_FROM_EMAIL, [user.email, ],
                             )
        email.send(fail_silently=True)
    return "Emails sent"
