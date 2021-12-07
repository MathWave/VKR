from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView


class UsersView(BaseView):
    endpoint = "users"

    def get(self):
        startswith = self.request.GET.get("startswith", "")
        return {
            "users": [
                user.username
                for user in User.objects.filter(
                    username__startswith=startswith
                ).order_by("username")
            ]
        }
