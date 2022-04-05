from Main.models import Set
from SprintLib.BaseView import BaseView, AccessError


class CheckersView(BaseView):
    required_login = True
    view_file = "checkers.html"
    endpoint = "polling/admin/checkers"
    set: Set

    def pre_handle(self):
        if (
            self.request.user != self.set.creator
            and self.request.user.username not in self.set.editors
        ):
            raise AccessError()
