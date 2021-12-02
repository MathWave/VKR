from SprintLib.BaseView import BaseView, AccessError


class SolutionView(BaseView):
    view_file = 'solution.html'
    required_login = True
    endpoint = "solution"

    def pre_handle(self):
        if self.request.user.is_superuser:
            return
        if self.entities.solution.user != self.request.user:
            raise AccessError()
