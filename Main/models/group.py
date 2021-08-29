from django.db import models
from Main.models.set import Set


class Group(models.Model):
    name = models.TextField()
    sets = models.ManyToManyField(Set)
