from django.db import models
from Main.models.task import Task


class File(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.TextField()
