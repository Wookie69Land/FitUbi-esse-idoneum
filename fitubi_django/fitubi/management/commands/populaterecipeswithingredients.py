from django.core.management.base import BaseCommand
from ._private import create_ingredients_for_recipe


class Command(BaseCommand):
    help = 'Populates recipes with ingredients'

    def handle(self, *args, **options):
        create_ingredients_for_recipe()
        self.stdout.write(self.style.SUCCESS("Successfully populated recipes with ingredients"))
