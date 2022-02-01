from SprintLib.BaseView import BaseView


class SolutionsView(BaseView):
    required_login = True
    endpoint = "solutions"
    view_file = "solutions.html"

    def get(self):
        self.context['task_id'] = self.request.GET.get('task_id')
        if not self.context['task_id']:
            self.context['set_id'] = self.request.GET['set_id']
