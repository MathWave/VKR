from django.contrib.auth import logout

from SprintLib.BaseView import BaseView


class ExitView(BaseView):
    required_login = True
    endpoint = "exit"

    def get(self):
        logout(self.request)
        return "/"
