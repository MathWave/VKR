from SprintLib.BaseView import BaseView


class ChatsView(BaseView):
    view_file = "chats.html"
    required_login = True
    endpoint = "chats"
