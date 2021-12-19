from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_chat")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_chat")
    user = None
