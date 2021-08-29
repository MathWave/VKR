from django.contrib.auth import logout

from SprintLib.BaseView import BaseView


class ExitView(BaseView):
    required_login = True

    def get(self):
        logout(self.request)
        return "/"
