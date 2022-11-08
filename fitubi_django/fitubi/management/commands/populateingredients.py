from django.core.management.base import BaseCommand
from ._private import create_ingredients

class Command(BaseCommand):
    help = 'Populates ingredients'

    def handle(self, *args, **options):
        create_ingredients()
        self.stdout.write(self.style.SUCCESS("Succesfully populated ingredients"))

