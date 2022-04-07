from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Main.models import Task


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    finished_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'task'])
        ]

    @property
    def time(self):
        if not self.finished:
            self.finished_time = timezone.now()
        return self.finished_time - self.start_time

    def increment_rating(self):
        if self.task.creator == self.user:
            return
        delta = timedelta(minutes=self.task.time_estimation)
        self.score = int(delta / self.time * 100)
        self.save()
        self.user.userinfo.refresh_from_db()
        self.user.userinfo.rating += self.score
        self.user.userinfo.save()

    @staticmethod
    def by_solution(solution):
        return Progress.objects.get(task=solution.task, user=solution.user)
