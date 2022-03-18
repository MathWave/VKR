from Main.models import Set
from SprintLib.BaseView import BaseView, AccessError


class CheckersView(BaseView):
    required_login = True
    view_file = "checkers.html"
    endpoint = "admin/checkers"
    set: Set

    def pre_handle(self):
        self.current_set = self.set
        if (
            self.request.user != self.current_set.creator
            and self.request.user.username not in self.current_set.editors
        ):
            raise AccessError()
