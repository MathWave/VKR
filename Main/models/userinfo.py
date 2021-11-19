from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Main.models.group import Group
from Main.models.settask import SetTask
from Main.models.subscription import Subscription
from Main.models.task import Task
from Sprint.settings import CONSTS


class UserInfo(models.Model):
    surname = models.TextField()
    name = models.TextField()
    middle_name = models.TextField()
    last_request = models.DateTimeField(default=timezone.now)
    profile_picture_fs_id = models.IntegerField(null=True)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    telegram_chat_id = models.TextField(default="")
    notification_solution_result = models.BooleanField(default=False)

    def _append_task(self, task, tasks):
        if task.creator == self.user or task.public or self.user.is_superuser:
            tasks.append(task)
            return
        for st in SetTask.objects.filter(task=task):
            if st.set.public:
                tasks.append(task)
                return
            for group in Group.objects.filter(sets=st.set):
                for sub in Subscription.objects.filter(group=group):
                    if sub.user == self.user:
                        tasks.append(task)
                        return

    @property
    def available_tasks(self):
        tasks = []
        for task in Task.objects.all():
            self._append_task(task, tasks)
        return sorted(tasks, key=lambda x: x.time_estimation)

    @property
    def place(self):
        return len(UserInfo.objects.filter(rating__gt=self.rating)) + 1

    @property
    def activity_status(self):
        if timezone.now() - self.last_request <= timezone.timedelta(minutes=5):
            return CONSTS["online_status"]
        return timezone.datetime.strftime(self.last_request, "%d-%m-%Y %H:%M")

    @property
    def can_create(self):
        # todo:
        return self.user.is_superuser

    @property
    def has_profile_pic(self):
        try:
            return self.profile_picture_fs_id is not None
        except ValueError:
            return False

    @property
    def profile_pic_url(self):
        if self.has_profile_pic:
            return "/image?id=" + str(self.profile_picture_fs_id)
        return "https://i2.wp.com/electrolabservice.com/wp-content/uploads/2021/01/blank-profile-picture-mystery-man-avatar-973460.jpg"

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.middle_name)
