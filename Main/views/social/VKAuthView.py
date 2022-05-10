import os
import random
import string

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from requests import get

from Main.models import UserInfo
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
            random_string = lambda: ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
            try:
                user = User.objects.get(userinfo__vk_user_id=user_id)
            except ObjectDoesNotExist:
                resp = get(f'https://api.vk.com/method/users.get?access_token={token}&user_ids={user_id}&v=5.131',
                           headers={"accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"})
                if resp.status_code != 200:
                    return "/enter"
                data = resp.json()['response'][0]
                user = User.objects.create_user(
                    username=random_string(),
                    email='',
                    password=random_string()
                )
                UserInfo.objects.create(
                    surname=data['last_name'],
                    name=data['first_name'],
                    vk_user_id=user_id,
                    user=user
                )
            login(self.request, user)
            return "/set_username"
        return "/enter"
