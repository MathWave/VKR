from django.contrib.auth import login
from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView


class SetUsernameView(BaseView):
    endpoint = "set_username"
    view_file = "set_username.html"
    required_login = False

    def get(self):
        if not self.request.user.is_authenticated:
            return "/"

    def post(self):
        if not self.request.user.is_authenticated:
            return "/"
        user = User.objects.filter(username=self.request.POST['username']).first()
        if user is None:
            self.request.user.username = self.request.POST['username']
            self.request.user.userinfo.verified = True
            self.request.user.save()
            self.request.user.userinfo.save()
            login(self.request, self.request.user)
            return "/"
        else:
            return "/set_username"
