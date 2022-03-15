from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .mixins import FileStorageMixin


class Dump(FileStorageMixin, models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    fs_id = models.IntegerField(null=True)
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, null=True)

    @property
    def ready(self):
        return self.fs_id is not None

    @property
    def str_date(self):
        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%S")

    @property
    def filename(self):
        if self.task is not None:
            return f"dump-task-{self.task.id}-{self.str_date}.zip"
