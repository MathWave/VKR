from django.http import HttpResponse

from Main.models import Solution
from Sprint.settings import CONSTS
from SprintLib.BaseView import BaseView


class SolutionsTableView(BaseView):
    view_file = 'solutions_table.html'
    required_login = True
    endpoint = "solutions_table"

    def get(self):
        self.context['solutions'] = Solution.objects.filter(
            user=self.request.user, task=self.entities.task
        ).order_by("-time_sent")
        if 'render' in self.request.GET.keys():
            return
        for sol in self.context['solutions']:
            if sol.result == CONSTS['testing_status'] or sol.result == CONSTS['in_queue_status']:
                return
        return HttpResponse('done')
