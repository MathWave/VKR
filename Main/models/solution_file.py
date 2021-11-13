from django.db import models

from Main.models.mixins import FileStorageMixin


class SolutionFile(FileStorageMixin, models.Model):
    path = models.TextField()
    fs_id = models.IntegerField()
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE)
