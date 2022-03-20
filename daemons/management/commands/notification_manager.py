from django.contrib.auth.models import User

from SprintLib.queue import MessagingSupport
from daemons.management.commands.bot import bot


class Command(MessagingSupport):
    help = "starts file notification manager"
    queue_name = "notifications"

    def process(self, payload: dict):
        user = User.objects.get(id=payload['user_id'])
        notification_type = payload['type']
        text = payload['text']
        if notification_type == "any" or getattr(user.userinfo, "notification_" + notification_type):
            bot.send_message(
                user.userinfo.telegram_chat_id,
                text,
                parse_mode="html",
            )
