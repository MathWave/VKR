from django.db.models import QuerySet

from Main.models import Solution
from SprintLib.BaseView import BaseView, AccessError


class SolutionsTableView(BaseView):
    view_file = "solutions_table.html"
    required_login = True
    endpoint = "solutions_table"
    page_size = 20
    page = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters = [
            self.filter_set,
            self.filter_task,
        ]
        self.queryset = Solution.objects.all()

    def filter_task(self, queryset: QuerySet):
        if 'task_id' in self.request.GET:
            return queryset.filter(task_id=int(self.request.GET['task_id']))
        return queryset

    def filter_set(self, queryset: QuerySet):
        if 'set_id' in self.request.GET:
            return queryset.filter(task__settasks__set_id=self.request.GET['set_id']).distinct()
        return queryset

    def pre_handle(self):
        if 'page' not in self.request.GET:
            raise AccessError()
        self.page = int(self.request.GET['page'])
        if "username" in self.request.GET and self.request.user.username == self.request.GET['username']:
            return
        if hasattr(self.entities, "set"):
            if self.entities.set.creator != self.request.user and self.request.user.username not in self.entities.set.editors:
                raise AccessError()
        if hasattr(self.entities, "task"):
            if self.entities.task.creator != self.request.user and self.request.user.username not in self.entities.task.editors:
                raise AccessError()

    def get(self):
        if 'only_my' in self.request.GET:
            self.queryset = self.queryset.filter(user=self.request.user)
        for fltr in self.filters:
            self.queryset = fltr(self.queryset)
        offset = self.page_size * (self.page - 1)
        limit = self.page_size
        self.context["solutions"] = self.queryset.order_by("-id")[offset:offset + limit]
        self.context["count_pages"] = range(1, (len(self.queryset) - 1) // self.page_size + 2)
        self.context["need_pagination"] = len(self.context["count_pages"]) > 1
