from django.db import models

from Main.models.task import Task
from Main.models.set import Set


class SetTask(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name="settasks")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="settasks")
    name = models.CharField(max_length=2)

    class Meta:
        indexes = [
            models.Index(fields=['set'])
        ]
