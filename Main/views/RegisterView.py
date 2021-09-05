from django.contrib.auth.models import User

from Main.models import UserInfo
from SprintLib.BaseView import BaseView


class RegisterView(BaseView):
    view_file = "register.html"
    required_login = False

    def get(self):
        self.context["error_message"] = self.request.GET.get("error_message", "")

    def post(self):
        data = self.request.POST
        if len(data["password"]) < 8:
            return "/register?error_message=Пароль слишком слабый"
        if data["password"] != data["repeat_password"]:
            return "/register?error_message=Пароли не совпадают"
        if len(User.objects.filter(username=data["username"])):
            return "/register?error_message=Данное имя пользователя уже занято"

        if len(User.objects.filter(email=data["email"])):
            return "/register?error_message=Пользователь под таким email уже зарегистрирован"
        user = User.objects.create_user(
            data["username"],
            data["email"],
            password=data["password"],
        )
        userinfo = UserInfo.objects.create(
            surname=data["surname"],
            name=data["name"],
            middle_name=data["middle_name"],
            user=user,
        )
        user.userinfo = userinfo
        user.save()
        # todo: реализовать подтверждение по почте
        return "/enter"
