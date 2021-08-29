from Main.models import Solution
from Sprint.celery import app
from SprintLib.testers import *


@app.task
def start_testing(solution_id):
    solution = Solution.objects.get(id=solution_id)
    eval(solution.language.work_name + 'Tester')(solution).execute()
