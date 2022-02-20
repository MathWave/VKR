from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Chat(models.Model):
    name = models.TextField()
    is_group = models.BooleanField()
    last_message = models.ForeignKey("Message", null=True, on_delete=models.SET_NULL, related_name='+')


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    time_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
