from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User

from Main.models.dump import Dump
from Main.models.extrafile import ExtraFile


class Task(models.Model):
    name = models.TextField()
    public = models.BooleanField(default=False)
    legend = models.TextField(default="")
    input_format = models.TextField(default="")
    output_format = models.TextField(default="")
    specifications = models.TextField(default="")
    time_limit = models.IntegerField(default=10000)
    time_estimation = models.IntegerField(default=5)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    editors = ArrayField(models.TextField(), default=list)
    allow_sharing = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def dumps(self):
        return Dump.objects.filter(task=self).order_by("-timestamp")

    @property
    def files(self):
        return ExtraFile.objects.filter(task=self, is_test=False)

    @property
    def tests(self):
        return ExtraFile.objects.filter(task=self, is_test=True).order_by('filename')

    @property
    def tests_count(self):
        return len(self.tests) // 2

    @property
    def samples(self):
        data = []
        for test in self.tests.order_by("test_number"):
            if test.is_sample and test.readable:
                data.append({"input": test.text, "output": test.answer.text})
        count = 1
        for entity in data:
            entity["num"] = count
            count += 1
        return data

    def delete(self, using=None, keep_parents=False):
        from Main.models.progress import Progress

        for progress in Progress.objects.filter(task=self):
            progress.user.userinfo.rating -= progress.score
            progress.user.userinfo.save()
        super().delete(using=using, keep_parents=keep_parents)
