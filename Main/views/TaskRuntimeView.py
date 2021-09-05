from django.http import HttpResponse

from Main.models import Progress
from SprintLib.BaseView import BaseView


class TaskRuntimeView(BaseView):
    view_file = 'task_runtime.html'
    required_login = True

    def get(self):
        progress = Progress.objects.get(task=self.entities.task, user=self.request.user)
        self.context['progress'] = progress
        if 'render' in self.request.GET.keys():
            return
        if progress.finished:
            return HttpResponse('done')
