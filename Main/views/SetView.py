from django.utils import timezone

from Main.models import Set
from SprintLib.BaseView import BaseView, AccessError


class SetView(BaseView):
    required_login = True
    endpoint = "set"
    view_file = "set.html"
    set: Set

    def get(self):
        if self.set in self.request.user.userinfo.available_sets:
            return
        if (
            not self.set.opened
            or self.set.start_time is not None
            and self.set.start_time > timezone.now()
            or self.set.end_time is not None
            and self.set.end_time < timezone.now()
        ):
            raise AccessError()
