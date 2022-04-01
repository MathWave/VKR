from subprocess import call

from SprintLib.queue import MessagingSupport


class Command(MessagingSupport):
    help = "starts docker cleaner"
    queue_name = "cleaner"

    def process(self, payload: dict):
        call(f'docker {payload["type"]} rm --force {payload["name"]}', shell=True)
