from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils import timezone

from Main.models.set import Set


class Group(models.Model):
    name = models.TextField()
    sets = models.ManyToManyField(Set)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User, related_name="user_groups")
    editors = ArrayField(models.TextField(), default=list)
    access_token = models.CharField(max_length=30, null=True, blank=True)

    @property
    def available_sets(self):
        return self.sets.filter(
            Q(opened=True)
            & (Q(start_time__isnull=True) | Q(start_time__lte=timezone.now()))
            & (Q(end_time__isnull=True) | Q(end_time__lte=timezone.now()))
        )
