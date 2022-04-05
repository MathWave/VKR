from typing import Optional

from Main.models import Solution, Set, Task, SetTask
from SprintLib.BaseView import BaseView, AccessError


class SolutionsTableView(BaseView):
    view_file = "solutions_table.html"
    required_login = True
    endpoint = "polling/solutions_table"
    page_size = 20
    page = None
    set: Optional[Set] = None
    task: Optional[Task] = None
    setTask: Optional[SetTask] = None

    def pre_handle(self):
        if 'page' not in self.request.GET:
            raise AccessError()
        self.page = int(self.request.GET['page'])
        if self.setTask is not None:
            self.set = self.setTask.set
            self.task = self.setTask.task

    def get(self):
        queryset = Solution.objects.all()
        if 'teacher' in self.request.GET.keys():
            if 'set_id' in self.request.GET.keys():
                if self.request.user != self.set.creator and self.request.user.username not in self.set.editors:
                    raise AccessError()
                queryset = queryset.filter(set_id=self.request.GET['set_id'])
            elif 'task_id' in self.request.GET.keys():
                if self.request.user != self.task.creator and self.request.user.username not in self.task.editors:
                    raise AccessError()
                queryset = queryset.filter(task_id=self.request.GET['task_id'], set=None)
            else:
                raise AccessError()
        else:
            queryset = queryset.filter(user=self.request.user, task=self.task, set=self.set)
        offset = self.page_size * (self.page - 1)
        limit = self.page_size
        self.context["solutions"] = queryset.order_by("-id")[offset:offset + limit]
        self.context["count_pages"] = range(1, (len(queryset) - 1) // self.page_size + 2)
        self.context["need_pagination"] = len(self.context["count_pages"]) > 1
