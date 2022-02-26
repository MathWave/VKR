from SprintLib.BaseView import BaseView


class SolutionsView(BaseView):
    required_login = True
    endpoint = "solutions"
    view_file = "solutions.html"

    def get(self):
        queries = []
        if 'task_id' in self.request.GET.keys():
            queries.append('task_id=' + self.request.GET['task_id'])
        if 'set_id' in self.request.GET.keys():
            queries.append('set_id=' + self.request.GET['set_id'])
            self.context['in_set'] = True
        else:
            self.context['in_set'] = False
        self.context['query'] = '&'.join(queries)
