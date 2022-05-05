from Main.models import Solution
from SprintLib.queue import MessagingSupport
from SprintLib.testers import *


class Command(MessagingSupport):
    help = "Tests solution"
    queue_name = "test"

    def process(self, payload: dict):
        id = payload['id']
        print(f"Received id {id}")
        solution = Solution.objects.get(id=id)
        tester = eval(solution.language.work_name + "Tester")(solution)
        try:
            tester.execute()
        except Exception as e:
            print(e)
            solution.result = "TE"
            solution.save()
