from subprocess import call, PIPE, run

from Main.models import Solution
from SprintLib.utils import LoopWorker


class Command(LoopWorker):
    help = "starts docker cleaner"

    def go(self):
        result = run("docker ps", universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        lines = result.stdout.split('\n')[1:]
        for line in lines:
            line = [i for i in line.split() if i]
            if line and line[-1].startswith('solution_'):
                for el in line[-1].split('_'):
                    if el.isnumeric():
                        solution_id = int(el)
                        break
                solution = Solution.objects.filter(id=solution_id).first()
                if solution is not None and (solution.result == 'In queue' or solution.result == 'Testing'):
                    continue
                call(f"docker rm --force {line[-1]}", shell=True)
        result = run("docker image ls", universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        lines = result.stdout.split('\n')[1:]
        for line in lines:
            line = [i for i in line.split() if i]
            if line and line[0].startswith('solution_'):
                call("docker image rm " + line[0], shell=True)
        result = run("docker network ls", universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        lines = result.stdout.split('\n')[1:]
        for line in lines:
            line = [i for i in line.split() if i]
            if line and line[1].startswith('solution_'):
                call("docker network rm " + line[0], shell=True)
        a = 5
        a += 1

    def handle(self, *args, **options):
        call('docker image rm $(docker images -q mathwave/sprint-repo)', shell=True)
        print("Old images removed")
        super().handle(*args, **options)

