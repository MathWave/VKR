from Main.models import Task
from SprintLib.BaseView import BaseView


class TasksView(BaseView):
    view_file = "tasks.html"
    required_login = True
    endpoint = "tasks"

    def get(self):
        self.context["tasks"] = Task.objects.filter(public=True).order_by('-time_estimation')

    def post(self):
        task_name = self.request.POST["name"]
        task = Task.objects.create(name=task_name, creator=self.request.user)
        return f"/admin/task?task_id={task.id}"
