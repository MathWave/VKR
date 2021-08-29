from os import remove
from os.path import join, exists

from django.db import models

from Sprint.settings import DATA_ROOT


class ExtraFile(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    filename = models.TextField()
    is_test = models.BooleanField(null=True)
    readable = models.BooleanField(null=True)
    test_number = models.IntegerField(null=True)

    @property
    def path(self):
        return join(DATA_ROOT, 'extra_files', str(self.id))

    @property
    def text(self):
        return open(self.path, 'r').read()

    def delete(self, using=None, keep_parents=False):
        if exists(self.path):
            remove(self.path)
        super().delete(using=using, keep_parents=keep_parents)
