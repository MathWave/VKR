import datetime
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from Checker.models import Checker


class Command(BaseCommand):
    help = "starts loop"

    def check_checkers(self):
        for checker in Checker.objects.filter(testing_solution__isnull=False, last_request__lt=timezone.now() - datetime.timedelta(seconds=3)):
            checker.testing_solution.result = 'In queue'
            checker.testing_solution.save()

    def handle(self, *args, **options):
        while True:
            self.check_checkers()
            sleep(5)
