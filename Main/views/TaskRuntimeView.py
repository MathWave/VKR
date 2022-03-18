from Main.models import Progress, Task
from SprintLib.BaseView import BaseView


class TaskRuntimeView(BaseView):
    view_file = "task_runtime.html"
    required_login = True
    endpoint = "task_runtime"
    task: Task

    def get(self):
        progress = Progress.objects.get(task=self.task, user=self.request.user)
        self.context["progress"] = progress
