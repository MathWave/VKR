from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from Main.models.set import Set


class Group(models.Model):
    name = models.TextField()
    sets = models.ManyToManyField(Set)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User, related_name='user_groups')
    editors = ArrayField(models.TextField(), default=list)

    @property
    def available_sets(self):
        return self.sets.filter(opened=True, start_time__lte=timezone.now(), end_time__gte=timezone.now())
