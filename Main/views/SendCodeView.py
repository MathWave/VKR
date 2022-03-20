from random import randrange

from django.contrib.auth import login
from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView
from SprintLib.queue import notify


class SendCodeView(BaseView):
    endpoint = "send_code"

    def post_create(self):
        username = self.request.POST["username"]
        user = User.objects.filter(username=username).first()
        if not user:
            return {
                "success": False,
                "message": "Пользователя с таким именем не существует",
            }
        code = randrange(10000, 100000)
        user.userinfo.code = code
        user.userinfo.save()
        notify(user, "any", "Код для входа в сервис: " + str(code))
        return {"success": True, "message": "Код отправлен"}

    def post_check(self):
        username = self.request.POST["username"]
        user = User.objects.filter(username=username).first()
        if not user:
            return {
                "success": False,
                "message": "Пользователя с таким именем не существует",
            }
        code = int(self.request.POST["code"])
        if code == user.userinfo.code:
            user.userinfo.code = None
            user.userinfo.save()
            login(self.request, user)
            return {"success": True, "message": "Успешно"}
        else:
            return {"success": False, "message": "Код неверен"}
