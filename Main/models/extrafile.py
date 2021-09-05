from os import remove
from os.path import join, exists

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from Sprint.settings import DATA_ROOT


class ExtraFile(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    filename = models.TextField()
    is_test = models.BooleanField(null=True)
    is_sample = models.BooleanField(null=True)
    readable = models.BooleanField(null=True)
    test_number = models.IntegerField(null=True)

    @property
    def path(self):
        return join(DATA_ROOT, "extra_files", str(self.id))

    @property
    def can_be_sample(self):
        return (
            self.is_test
            and not self.filename.endswith(".a")
            and len(
                ExtraFile.objects.filter(task=self.task, filename=self.filename + ".a")
            )
        )

    @property
    def text(self):
        return open(self.path, "r").read()

    def delete(self, using=None, keep_parents=False):
        if exists(self.path):
            remove(self.path)
        if self.is_test and self.filename.endswith('.a'):
            try:
                ef = ExtraFile.objects.get(task=self.task, filename=self.filename.rstrip('.a'), is_test=True)
                ef.is_sample = False
                ef.save()
            except ObjectDoesNotExist:
                pass
        super().delete(using=using, keep_parents=keep_parents)

    @property
    def answer(self):
        return ExtraFile.objects.get(task=self.task, is_test=True, filename=self.filename + '.a')