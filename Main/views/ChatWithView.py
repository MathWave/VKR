from django.contrib.auth.models import User
from django.db.models import Q

from Main.models import Chat
from SprintLib.BaseView import BaseView, AccessError


class ChatWithView(BaseView):
    required_login = True
    endpoint = "chat_with"
    chat = None

    def pre_handle(self):
        if "username" not in self.request.GET:
            raise AccessError()

    def get(self):
        chat = Chat.objects.filter(
            Q(
                from_user=self.request.user,
                to_user__username=self.request.GET["username"],
            )
            | Q(
                to_user=self.request.user,
                from_user__username=self.request.GET["username"],
            )
        ).first()
        if chat is None:
            chat = Chat.objects.create(from_user=self.request.user, to_user=User.objects.get(username=self.request.GET['username']))
        return "/chat?chat_id=" + str(chat.id)
