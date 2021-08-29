from django.contrib.auth.models import User
from django.db import models


class Set(models.Model):
    name = models.TextField()
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
