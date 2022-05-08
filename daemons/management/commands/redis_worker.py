from SprintLib.queue import MessagingSupport
from SprintLib.redis import lock, get_redis


class Command(MessagingSupport):
    help = "Starts redis worker"
    queue_name = "redis"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers = {
            "docker": self.docker_handler
        }

    @lock("docker")
    def docker_handler(self, payload):
        key = payload["key"]
        value = payload["value"]
        with get_redis() as r:
            r.lpush(key, value)

    def process(self, payload: dict):
        action = payload.get("action")
        if action is None:
            raise ValueError("No action field in message")
        handler = self.handlers.get(action)
        if handler is None:
            raise ValueError(f"No handler for action: {action}")
        handler(payload)
