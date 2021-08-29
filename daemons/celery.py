from SprintLib.BaseDaemon import BaseDaemon


class Daemon(BaseDaemon):
    def command(self):
        return "celery -A Sprint worker -l INFO --concurrency=4"
