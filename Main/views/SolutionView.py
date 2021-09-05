from SprintLib.BaseView import BaseView, AccessError


class SolutionView(BaseView):
    view_file = 'solution.html'
    required_login = True

    def pre_handle(self):
        if self.entities.solution.user != self.request.user:
            raise AccessError()
