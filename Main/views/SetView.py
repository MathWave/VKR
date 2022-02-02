from django.utils import timezone

from SprintLib.BaseView import BaseView, AccessError


class SetView(BaseView):
    required_login = True
    endpoint = "set"
    view_file = "set.html"

    def get(self):
        if self.entities.set in self.request.user.userinfo.available_sets:
            return
        if (
            not self.entities.set.opened
            or self.entities.set.start_time is not None
            and self.entities.set.start_time > timezone.now()
            or self.entities.set.end_time is not None
            and self.entities.set.end_time < timezone.now()
        ):
            raise AccessError()
