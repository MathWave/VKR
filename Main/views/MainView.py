from random import sample

from django.db.models import Count, Max
from django.utils import timezone

from Main.models import Task, UserInfo, Solution
from SprintLib.BaseView import BaseView


class MainView(BaseView):
    view_file = "main.html"
    required_login = True
    endpoint = ""

    def get(self):
        self.context['top_tasks_today'] = Task.objects.filter(public=True, solution__time_sent__date=timezone.now().date()).annotate(count=Count('solution__task_id')).order_by('-count')[:5]
        if len(self.context['top_tasks_today']) < 5:
            self.context['top_tasks_today'] = Task.objects.filter(public=True, solution__time_sent__isnull=False).annotate(time_sent=Max('solution__time_sent'), count=Count('solution__task_id')).order_by('-count', '-time_sent')[:5]
        if len(self.context['top_tasks_today']) < 5:
            self.context['top_tasks_today'] = Task.objects.filter(public=True).order_by('name')[:5]
        for task in self.context['top_tasks_today']:
            setattr(task, 'solution', Solution.objects.filter(user=self.request.user, task=task).first())
        self.context['top_users'] = UserInfo.objects.filter(verified=True).order_by('-rating')[:5]
        all_tasks = Task.objects.filter(solution__user=self.request.user).distinct()
        ok_tasks = all_tasks.filter(solution__result="OK").distinct()
        undone_tasks = set(all_tasks) - set(ok_tasks)
        self.context['undone_tasks'] = sample(undone_tasks, k=min(5, len(undone_tasks)))
        for task in self.context['undone_tasks']:
            setattr(task, 'solution', Solution.objects.filter(user=self.request.user, task=task).first())
        new_tasks = set(Task.objects.filter(public=True)) - set(all_tasks)
        self.context['new_tasks'] = sample(new_tasks, k=min(5, len(new_tasks)))
