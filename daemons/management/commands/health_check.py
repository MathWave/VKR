from time import sleep

from django.core.management.base import BaseCommand
from django.db import connections, OperationalError
from requests import get

from daemons.management.commands.bot import bot


class Command(BaseCommand):
    help = "starts health check"

    def go(self):
        db_conn = connections["default"]
        try:
            db_conn.cursor()
        except OperationalError:
            connected = False
        else:
            connected = True
        if not connected:
            bot.send_message(84367486, "База сдохла")
            return
        web_working = True
        try:
            code = get("http://dev.sprinthub.ru/").status_code
            if code != 200:
                web_working = False
        except:
            web_working = False
        if not web_working:
            bot.send_message(84367486, "Сайт сдох")
            return
        try:
            get("http://dev.sprinthub.ru:5555")
        except:
            bot.send_message(84367486, "Файловое хранилище сдохло")

    def handle(self, *args, **options):
        sleep(60 * 5)
        while True:
            self.go()
            sleep(60 * 30)
