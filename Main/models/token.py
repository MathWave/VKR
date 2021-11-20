from random import choice

from django.db.models import JSONField
from django.db import models
from django.utils import timezone


def create_token():
    symbols = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    return "".join([choice(symbols) for _ in range(30)])


class Token(models.Model):
    token = models.CharField(max_length=30, default=create_token)
    created_dt = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=20)
    extras = JSONField()
