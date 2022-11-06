from django.core.management.base import BaseCommand
from ._private import create_students, create_subjects


class Command(BaseCommand):
    help = 'Populates school with students, subjects and teachers'

    def handle(self, *args, **options):
        create_students()
        self.stdout.write(self.style.SUCCESS("Succesfully populated school with students"))
        create_subjects()
        self.stdout.write(self.style.SUCCESS("Succesfully created subjects"))
