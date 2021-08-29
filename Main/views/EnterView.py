from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from SprintLib.BaseView import BaseView


class EnterView(BaseView):
    view_file = "enter.html"
    required_login = False

    def get(self):
        self.context["error_message"] = self.request.GET.get("error_message", "")

    def post(self):
        try:
            user = User.objects.get(username=self.request.POST["email"])
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(email=self.request.POST["email"])
            except ObjectDoesNotExist:
                return "/enter?error_message=Данного пользователя не существует"
        user = authenticate(
            username=user.username, password=self.request.POST["password"].strip()
        )
        if user is not None:
            login(self.request, user)
            return "/"
        return "/enter?error_message=Неверный пароль"
