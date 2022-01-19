from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Main.models.chat import Chat


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
    time_sent = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['chat', '-time_sent'])
        ]
