from SprintLib.BaseView import BaseView


class SolutionsView(BaseView):
    required_login = True
    endpoint = "solutions"
    view_file = "solutions.html"

    def get(self):
        self.context["username"] = self.request.GET.get("username")
        self.context["task_id"] = self.request.GET.get("task_id")
        if self.context["task_id"]:
            self.context["task_id"] = int(self.context["task_id"])
        self.context["set_id"] = self.request.GET.get("set_id")
        if self.context["set_id"]:
            self.context["set_id"] = int(self.context["set_id"])
