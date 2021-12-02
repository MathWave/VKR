from django.core.management.base import BaseCommand
from FileStorage.root import runserver


class Command(BaseCommand):
    help = "starts FileStorage"

    def handle(self, *args, **options):
        runserver()
