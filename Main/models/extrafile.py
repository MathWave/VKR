from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .mixins import FileStorageMixin


class ExtraFile(FileStorageMixin, models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    filename = models.TextField()
    is_test = models.BooleanField(null=True)
    is_sample = models.BooleanField(null=True)
    readable = models.BooleanField(null=True)
    test_number = models.IntegerField(null=True)
    fs_id = models.IntegerField(null=True)

    @property
    def can_be_sample(self):
        return (
            self.is_test
            and not self.filename.endswith(".a")
            and len(
                ExtraFile.objects.filter(task=self.task, filename=self.filename + ".a")
            )
        )

    def delete(self, using=None, keep_parents=False):
        self.remove_from_fs()
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
