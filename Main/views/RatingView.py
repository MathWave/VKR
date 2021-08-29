from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView


class RatingView(BaseView):
    view_file = "rating.html"
    required_login = True

    def get(self):
        self.context["users"] = User.objects.all().order_by('-userinfo__rating')
