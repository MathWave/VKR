from SprintLib.queue import MessagingSupport
from daemons.management.commands.bot import bot


class Command(MessagingSupport):
    help = "starts file telegram sender"
    queue_name = "telegram"

    def process(self, payload: dict):
        chat_id = payload['chat_id']
        text = payload['text']
        bot.send_message(
            int(chat_id),
            text,
            parse_mode="html",
        )
