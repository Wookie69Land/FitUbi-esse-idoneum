from django.core.management.base import BaseCommand
from ._private import create_recipe


class Command(BaseCommand):
    help = 'Populates recipes'

    def handle(self, *args, **options):
        create_recipe()
        self.stdout.write(self.style.SUCCESS("Successfully populated recipes"))
