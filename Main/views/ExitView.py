from django.contrib.auth import logout

from SprintLib.BaseView import BaseView


class ExitView(BaseView):
    required_login = True
    endpoint = "logout"

    def get(self):
        logout(self.request)
        return "/"
