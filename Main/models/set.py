from functools import cached_property

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from Main.models.task import Task


class Set(models.Model):
    name = models.TextField()
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    opened = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    editors = ArrayField(models.TextField(), default=list)


    @property
    def available(self):
        return (
            self.opened
            and (self.start_time is None or timezone.now() >= self.start_time)
            and (self.end_time is None or timezone.now() <= self.end_time)
        )

    @cached_property
    def tasks(self):
        return Task.objects.filter(settasks__set=self).order_by("settasks__name")
