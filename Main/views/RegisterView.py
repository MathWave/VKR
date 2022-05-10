from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q

from Main.models import UserInfo
from SprintLib.BaseView import BaseView


class RegisterView(BaseView):
    view_file = "register.html"
    required_login = False
    endpoint = "register"

    def post(self):
        username = self.request.POST['username']
        email = self.request.POST['email']
        surname = self.request.POST['surname']
        name = self.request.POST['name']
        password = self.request.POST['password']
        if User.objects.filter(Q(email=email) | Q(username=username)):
            return '/register'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        UserInfo.objects.create(
            surname=surname,
            name=name,
            user=user,
            verified=True
        )
        login(self.request, user)
        return "/"
