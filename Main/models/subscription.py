from django.db import models
from django.contrib.auth.models import User

from Main.models.group import Group


class Subscription(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="subscriptions"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField()
