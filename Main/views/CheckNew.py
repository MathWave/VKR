from django.contrib.auth.models import User
from django.http import HttpResponse

from SprintLib.BaseView import BaseView


class CheckNew(BaseView):
    endpoint = "check_new"

    def post_check_username(self):
        username = self.request.POST['username']
        user = User.objects.filter(username=username).first()
        if len(username) < 8:
            user = 'incorrect'
        return HttpResponse(status=400 if user else 200)

    def post_check_email(self):
        email = self.request.POST['email']
        user = User.objects.filter(email=email).first()
        if email.count('.') == 0 or email.count('@') != 1:
            user = 'incorrect'
        if email.find('@') > email.rfind('.'):
            user = 'incorrect'
        return HttpResponse(status=400 if user else 200)
