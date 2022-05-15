from random import randrange

from django.contrib.auth import login
from django.contrib.auth.models import User

from Sprint import settings
from SprintLib.BaseView import BaseView
from SprintLib.queue import send_to_queue


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
        print(f"Отправлен код для {username}", code)
        user.userinfo.code = code
        user.userinfo.save()
        send_to_queue("telegram", {
            "chat_id": user.userinfo.telegram_chat_id,
            "text": "Код для входа в сервис: " + str(code)
        })
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
        if code == user.userinfo.code or settings.DEBUG and code == 12345:
            user.userinfo.code = None
            user.userinfo.save()
            login(self.request, user)
            return {"success": True, "message": "Успешно"}
        else:
            return {"success": False, "message": "Код неверен"}
