import datetime

from django.utils import timezone

from Checker.models import Checker
from SprintLib.utils import LoopWorker


class Command(LoopWorker):
    help = "starts loop"

    def go(self):
        for checker in Checker.objects.filter(testing_solution__isnull=False, last_request__lt=timezone.now() - datetime.timedelta(seconds=3)):
            checker.testing_solution.result = 'In queue'
            checker.testing_solution.save()
