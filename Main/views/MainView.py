from random import sample

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max, Q
from django.utils import timezone

from Checker.models import Checker
from Main.models import Task, UserInfo, Solution, Group
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.language import languages


class MainView(BaseView):
    endpoint = ""

    @property
    def view_file(self):
        if self.request.user.is_authenticated and self.request.user.userinfo.verified:
            return "main.html"
        return "landing.html"

    def get_main(self):
        self.context['top_tasks_today'] = Task.objects.filter(public=True,
                                                              solution__time_sent__date=timezone.now().date()).annotate(
            count=Count('solution__task_id')).order_by('-count')[:5]
        if len(self.context['top_tasks_today']) < 5:
            self.context['top_tasks_today'] = Task.objects.filter(public=True,
                                                                  solution__time_sent__isnull=False).annotate(
                time_sent=Max('solution__time_sent'), count=Count('solution__task_id')).order_by('-count',
                                                                                                 '-time_sent')[:5]
        if len(self.context['top_tasks_today']) < 5:
            self.context['top_tasks_today'] = Task.objects.filter(public=True).order_by('name')[:5]
        for task in self.context['top_tasks_today']:
            setattr(task, 'solution', Solution.objects.filter(user=self.request.user, task=task, set=None).last())
        self.context['top_users'] = UserInfo.objects.filter(verified=True).order_by('-rating')[:5]
        all_tasks = Task.objects.filter(solution__user=self.request.user).distinct()
        ok_tasks = all_tasks.filter(solution__result="OK").distinct()
        undone_tasks = set(all_tasks) - set(ok_tasks)
        self.context['undone_tasks'] = sample(undone_tasks, k=min(5, len(undone_tasks)))
        for task in self.context['undone_tasks']:
            setattr(task, 'solution', Solution.objects.filter(user=self.request.user, task=task).last())
        new_tasks = set(Task.objects.filter(public=True)) - set(all_tasks)
        self.context['new_tasks'] = sample(new_tasks, k=min(5, len(new_tasks)))
        self.context['groups'] = Group.objects.filter(
            Q(editors__in=self.request.user.username) | Q(creator=self.request.user) | Q(
                users=self.request.user)).distinct()

    def get_landing(self):
        self.context['solutions'] = len(Solution.objects.all())
        self.context['tasks'] = len(Task.objects.all())
        self.context['users'] = len(UserInfo.objects.all())
        self.context['languages'] = len(languages)
        self.context['groups'] = len(Group.objects.all())
        self.context['runners'] = len(Checker.objects.all())

    def get(self):
        if self.request.user.is_authenticated:
            return self.get_main()
        return self.get_landing()

    def post(self):
        if not self.request.user.userinfo.teacher:
            raise AccessError()
        group = Group.objects.create(name=self.request.POST['name'], creator=self.request.user)
        return '/group?group_id=' + str(group.id)

    def post_token(self):
        token = self.request.POST['token']
        try:
            group = Group.objects.get(access_token=token)
            group.users.add(self.request.user)
            return '/group?group_id=' + str(group.id)
        except ObjectDoesNotExist:
            return "/"
