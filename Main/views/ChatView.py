from typing import Optional

from Main.management.commands.bot import bot
from Main.models import Chat, Message
from Sprint.settings import CONSTS
from SprintLib.BaseView import BaseView


class ChatView(BaseView):
    endpoint = "chat"
    required_login = True
    view_file = "chat.html"
    chat: Optional[Chat] = None

    def pre_handle(self):
        if self.entities.chat.from_user == self.request.user:
            self.entities.chat.user = self.entities.chat.to_user
        else:
            self.entities.chat.user = self.entities.chat.from_user

    def post(self):
        Message.objects.create(
            user=self.request.user,
            chat=self.entities.chat,
            text=self.request.POST["text"],
        )
        if (
            self.entities.chat.user.userinfo.activity_status != CONSTS["online_status"]
            and self.entities.chat.user.userinfo.notification_messages
        ):
            bot.send_message(
                self.entities.chat.user.userinfo.telegram_chat_id,
                f"Пользователь {self.request.user.username} отправил сообщение:\n"
                f"{self.request.POST['text']}",
            )
        return "/chat?chat_id" + str(self.entities.chat.id)
