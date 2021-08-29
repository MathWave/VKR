from os import mkdir
from os.path import join, exists
from shutil import rmtree
from subprocess import call

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Main.models.task import Task
from Main.models.language import Language
from Sprint.settings import CONSTS, SOLUTIONS_ROOT


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    time_sent = models.DateTimeField(default=timezone.now)
    result = models.TextField(default=CONSTS["in_queue_status"])

    def delete(self, using=None, keep_parents=False):
        if exists(self.directory):
            rmtree(self.directory)
        super().delete(using=using, keep_parents=keep_parents)

    def create_dirs(self):
        mkdir(self.directory)
        mkdir(self.testing_directory)

    @property
    def directory(self):
        return join(SOLUTIONS_ROOT, str(self.id))

    @property
    def testing_directory(self):
        return join(self.directory, 'test_dir')

    def exec_command(self, command, working_directory='app', timeout=None):
        return call(f'docker exec -i solution_{self.id} bash -c "cd {working_directory} && {command}"', shell=True, timeout=timeout)
