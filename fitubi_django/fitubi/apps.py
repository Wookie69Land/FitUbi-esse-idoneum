from django.apps import AppConfig


class FibubiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitubi'

    def ready(self):
        from fitubi.models import create_user_profile
