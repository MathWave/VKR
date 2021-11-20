from django.contrib.auth import login

from Main.management.commands.bot import bot
from SprintLib.BaseView import BaseView
from django.contrib.auth.models import User
from random import randrange


class SendCodeView(BaseView):
    def post_create(self):
        username = self.request.POST["username"]
        user = User.objects.filter(username=username).first()
        if not user:
            return {"success": False, "message": "Пользователя с таким именем не существует"}
        code = randrange(10000, 100000)
        user.userinfo.code = code
        user.userinfo.save()
        bot.send_message(user.userinfo.telegram_chat_id, "Код для входа в сервис: " + str(code))
        return {"success": True, "message": "Код отправлен"}

    def post_check(self):
        username = self.request.POST["username"]
        user = User.objects.filter(username=username).first()
        if not user:
            return {"success": False, "message": "Пользователя с таким именем не существует"}
        code = int(self.request.POST["code"])
        if code == user.userinfo.code:
            login(self.request, user)
            return {"success": True, "message": "Успешно"}
        else:
            return {"success": False, "message": "Код неверен"}
