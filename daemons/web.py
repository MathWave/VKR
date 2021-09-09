from SprintLib.BaseDaemon import BaseDaemon


class Daemon(BaseDaemon):
    def command(self):
        return "python manage.py runserver 0.0.0.0:443"
