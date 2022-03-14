from os.path import join, exists
from shutil import rmtree

from Main.models import Solution
from SprintLib.queue import MessagingSupport
from SprintLib.testers import *


class Command(MessagingSupport):
    help = "Tests solution"
    queue_name = "test"

    def consume(self, ch, method, properties, body):
        id = int(str(body, encoding="utf-8"))
        print(f"Received id {id}")
        solution = Solution.objects.get(id=id)
        try:
            eval(solution.language.work_name + "Tester")(solution).execute()
        except Exception as e:
            print(e)
            solution.result = "TE"
            solution.save()
        finally:
            path = join("solutions", str(id))
            if exists(path):
                rmtree(path)
