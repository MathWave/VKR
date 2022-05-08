from subprocess import call

from django.db.models import Q

from Main.models import Solution
from SprintLib.utils import LoopWorker


class Command(LoopWorker):
    help = "starts docker cleaner"

    def go(self):
        for solution in Solution.objects.filter(~Q(result="Testing") | ~Q(result="In queue"), docker_instances__isnull=False):
            for instance in sorted(solution.docker_instances, key=lambda x: x['type']):
                if instance['type'] == 'network':
                    call(f"docker network rm --force {instance['name']}", shell=True)
                elif instance['type'] == 'image':
                    call(f"docker image rm --force {instance['name']}", shell=True)
                elif instance['type'] == 'container':
                    call(f"docker rm --force {instance['name']}", shell=True)
                else:
                    raise ValueError(f"Unknown docker type {instance['type']}")
            solution.docker_instances = None
            solution.save()

    def handle(self, *args, **options):
        call('docker image rm $(docker images -q mathwave/sprint-repo)', shell=True)
        print("Old images removed")
        super().handle(*args, **options)

