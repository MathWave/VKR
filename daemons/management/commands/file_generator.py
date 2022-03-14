from SprintLib.queue import MessagingSupport


class Command(MessagingSupport):
    help = "starts file generator"
    queue_name = "files"

    def consume(self, ch, method, properties, body):
        ...