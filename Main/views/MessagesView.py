from Main.models import Message
from SprintLib.BaseView import BaseView, AccessError


class MessagesView(BaseView):
    required_login = True
    view_file = "messages.html"
    endpoint = "messages"
    page_size = 20

    def pre_handle(self):
        if not hasattr(self.entities, "chat") or 'page' not in self.request.GET:
            raise AccessError()
        if self.entities.chat.from_user != self.request.user and self.entities.chat.to_user != self.request.user:
            raise AccessError()

    def get(self):
        offset = (int(self.request.GET["page"]) - 1) * self.page_size
        limit = self.page_size
        messages = Message.objects.filter(chat=self.entities.chat).order_by("-time_sent")
        messages.update(read=True)
        self.context["messages"] = messages[offset:offset + limit]
        self.context["count_pages"] = range(1, (len(messages) - 1) // self.page_size + 2)
        self.context["need_pagination"] = len(self.context["count_pages"]) > 1
