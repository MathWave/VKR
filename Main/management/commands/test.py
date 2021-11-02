from django.core.management.base import BaseCommand

from Main.models import Solution
from SprintLib.testers import *


class Command(BaseCommand):
    help = 'Tests solution'

    def add_arguments(self, parser):
        parser.add_argument('solution_id', type=int)

    def handle(self, *args, **options):
        solution = Solution.objects.get(id=options['solution_id'])
        eval(solution.language.work_name + 'Tester')(solution).execute()
