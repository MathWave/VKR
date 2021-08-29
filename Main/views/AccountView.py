from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView


class AccountView(BaseView):
    view_file = "account.html"
    required_login = True

    def get(self):
        if "username" in self.request.GET.keys():
            self.context["account"] = User.objects.get(
                username=self.request.GET["username"]
            )
        else:
            self.context["account"] = self.request.user
        self.context["owner"] = self.context["account"] == self.request.user
        self.context["error_message"] = self.request.GET.get("error_message", "")

    def post_upload_photo(self):
        self.request.user.userinfo.profile_picture.delete()
        self.request.user.userinfo.profile_picture = self.request.FILES["file"]
        self.request.user.userinfo.save()
        return "/account"

    def post_change_password(self):
        password = self.request.POST["password"].strip()
        new_password = self.request.POST["new_password"].strip()
        user = authenticate(username=self.request.user.username, password=password)
        if not user:
            return "/account?error_message=Неправильно указан пароль"
        if len(new_password) < 8:
            return "/account?error_message=Пароль слишком слабый"
        if new_password != self.request.POST["repeat"]:
            return "/account?error_message=Пароли не совпадают"
        self.request.user.set_password(new_password)
        self.request.user.save()
        login(self.request, self.request.user)
        return "/account?error_message=Пароль успешно установлен"
