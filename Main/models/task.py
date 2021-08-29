from django.db import models
from django.contrib.auth.models import User

from Main.models.extrafile import ExtraFile


class Task(models.Model):
    name = models.TextField()
    public = models.BooleanField(default=False)
    legend = models.TextField(default="")
    input_format = models.TextField(default="")
    output_format = models.TextField(default="")
    specifications = models.TextField(default="")
    time_limit = models.IntegerField(default=10000)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    @property
    def files(self):
        return ExtraFile.objects.filter(task=self, is_test=False)

    @property
    def tests(self):
        return ExtraFile.objects.filter(task=self, is_test=True)
