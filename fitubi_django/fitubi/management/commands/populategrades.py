from django.core.management.base import BaseCommand
from ._private import create_grade

class Command(BaseCommand):
    help = 'Populates students with grades for every subject'

    def handle(self, *args, **options):
        create_grade()
        self.stdout.write(self.style.SUCCESS("Succesfully populated students with grades"))

