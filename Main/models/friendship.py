from django.contrib.auth.models import User
from django.db import models


class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_friendship")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_friendship")
    verified = models.BooleanField(default=False)
