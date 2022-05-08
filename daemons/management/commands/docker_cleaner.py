from subprocess import call

from SprintLib.redis import lock, get_redis
from SprintLib.utils import LoopWorker


class Command(LoopWorker):
    help = "starts docker cleaner"

    @lock("docker")
    def go(self):
        containers, images, networks = list(), list(), list()
        with get_redis() as r:
            while r.llen("containers") != 0:
                value = r.rpop("containers").decode("utf-8")
                return_code = call(f"docker rm --force {value}", shell=True)
                if return_code != 0:
                    containers.append(value)
            while r.llen("images") != 0:
                value = r.rpop("images").decode("utf-8")
                return_code = call(f"docker image rm --force {value}", shell=True)
                if return_code != 0:
                    images.append(value)
            while r.llen("networks") != 0:
                value = r.rpop("networks").decode("utf-8")
                return_code = call(f"docker network rm {value}", shell=True)
                if return_code != 0:
                    networks.append(value)
            if containers:
                r.lpush("containers", *containers)
            if images:
                r.lpush("images", *images)
            if networks:
                r.lpush("networks", *networks)

    def handle(self, *args, **options):
        call('docker image rm $(docker images -q mathwave/sprint-repo)', shell=True)
        print("Old images removed")
        super().handle(*args, **options)

