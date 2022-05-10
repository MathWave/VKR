from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q

from SprintLib.BaseView import BaseView


class TelegramEnterView(BaseView):
    view_file = "telegram_enter.html"
    required_login = False
    endpoint = "telegram_enter"

    def post(self):
        username = self.request.POST['username']
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user is None:
            return "/enter"
        user = authenticate(username=user.username, password=self.request.POST['password'])
        if user is None:
            return "/enter"
        login(self.request, user)
        return "/"
