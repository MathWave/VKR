from django.contrib.auth.models import User
from django.core.management import BaseCommand

from Main.management.commands.bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.filter(is_superuser=True):
            bot.send_message(user.userinfo.telegram_chat_id, "Деплой прошел успешно")
