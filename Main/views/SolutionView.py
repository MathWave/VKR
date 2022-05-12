from Main.models import Solution
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.utils import send_testing


class SolutionView(BaseView):
    view_file = "solution.html"
    required_login = True
    endpoint = "solution"
    solution: Solution

    def check_admin(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return True
        if self.solution.task.creator == user or user.username in self.solution.task.editors:
            return True
        if self.solution.set:
            if self.solution.set.creator == user or user.username in self.solution.set.editors:
                return True
        return False

    def pre_handle(self):
        if self.check_admin():
            return
        if self.solution.user != self.request.user:
            raise AccessError()

    def post_retest(self):
        if not self.check_admin():
            return "/"
        send_testing(self.solution)
        return "/solution?solution_id=" + str(self.solution.id)
