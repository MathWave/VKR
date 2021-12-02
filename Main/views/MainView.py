from SprintLib.BaseView import BaseView


class MainView(BaseView):
    view_file = "main.html"
    required_login = True
    endpoint = ""
