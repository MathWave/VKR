from subprocess import call

from SprintLib.queue import MessagingSupport


class Command(MessagingSupport):
    help = "starts docker cleaner"
    queue_name = "cleaner"

    def handle(self, *args, **options):
        call('docker image rm $(docker images -q mathwave/sprint-repo)', shell=True)
        print("Old images removed")
        super().handle(*args, **options)

    def process(self, payload: dict):
        name = payload['name']
        type = payload['type']
        if type == 'network':
            command = f'docker network rm {name}'
        elif type == 'container':
            command = f'docker rm --force {name}'
        elif type == 'image':
            command = f'docker image rm --force {name}'
        else:
            raise NotImplementedError(f"Unknown type {type}")
        print(f"Executing command {command}")
        code = call(command, shell=True)
        if code == 0:
            print(f"Removed {type} {name}")
        else:
            print("Something went wrong")
