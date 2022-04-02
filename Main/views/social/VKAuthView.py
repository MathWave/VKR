import os

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from requests import get

from SprintLib.BaseView import BaseView


class VKAuthView(BaseView):
    required_login = False
    endpoint = "vk_auth"
    view_file = "vk_auth.html"
    fields_except = ('user_id',)

    def get(self):
        if not self.request.GET:
            return
        access_token = self.request.GET['access_token']
        token = os.getenv("VK_SERVICE_TOKEN")
        resp = get(f'https://api.vk.com/method/secure.checkToken?token={access_token}&access_token={token}&v=5.131').json()
        if 'response' in resp and 'success' in resp['response'] and resp['response']['success'] == 1:
            user_id = resp['response']['user_id']
            try:
                user = User.objects.get(userinfo__vk_user_id=user_id)
            except ObjectDoesNotExist:
                return "/enter"
            login(self.request, user)
            return "/"
        return "/enter"
