from Main.models import Solution
from SprintLib.BaseView import BaseView, AccessError


class SolutionView(BaseView):
    view_file = "solution.html"
    required_login = True
    endpoint = "solution"
    solution: Solution

    def pre_handle(self):
        if self.request.user.is_superuser:
            return
        if self.solution.user != self.request.user:
            raise AccessError()
