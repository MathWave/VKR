from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView


class RatingView(BaseView):
    view_file = "rating.html"
    required_login = True
    endpoint = "rating"

    def get(self):
        self.context["users"] = User.objects.filter(userinfo__verified=True).order_by(
            "-userinfo__rating", "-date_joined"
        )
