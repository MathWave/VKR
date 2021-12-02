from SprintLib.BaseView import BaseView


class EnterView(BaseView):
    view_file = "enter.html"
    required_login = False
    endpoint = "enter"
