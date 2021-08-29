from Main.models import Set
from SprintLib.BaseView import BaseView


class SetsView(BaseView):
    view_file = "sets.html"
    required_login = True

    def post(self):
        task_name = self.request.POST["name"]
        task = Set.objects.create(name=task_name, creator=self.request.user)
        return f"/admin/task?task_id={task.id}"
