from functools import cached_property

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.functions import Length
from django.utils import timezone

from Main.models.task import Task


class Set(models.Model):
    name = models.TextField()
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    opened = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=None, null=True)
    end_time = models.DateTimeField(default=None, null=True)
    editors = ArrayField(models.TextField(), default=list)
    description = models.TextField(default='')

    @property
    def start_time_moscow(self):
        if self.start_time is None:
            return None
        return self.start_time.astimezone(timezone.get_current_timezone())

    @property
    def end_time_moscow(self):
        if self.end_time is None:
            return None
        return self.end_time.astimezone(timezone.get_current_timezone())

    @property
    def start_time_format(self):
        if self.start_time is None:
            return None
        return self.start_time_moscow.strftime("%Y-%m-%dT%H:%M")

    @property
    def end_time_format(self):
        if self.end_time is None:
            return None
        return self.end_time_moscow.strftime("%Y-%m-%dT%H:%M")

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

    @cached_property
    def settasks_ordered(self):
        return self.settasks.order_by(Length('name'), 'name')
