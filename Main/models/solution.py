from functools import cached_property
from os.path import exists
from shutil import rmtree
from subprocess import call

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Main.models import Set
from Main.models.solution_file import SolutionFile
from Main.models.task import Task
from Sprint.settings import CONSTS
from SprintLib.language import languages


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language_id = models.IntegerField(default=0)
    time_sent = models.DateTimeField(default=timezone.now)
    result = models.TextField(default=CONSTS["in_queue_status"])
    test = models.IntegerField(default=None, null=True)
    set = models.ForeignKey(Set, null=True, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=['task', 'user', '-time_sent']),
            models.Index(fields=['task', '-time_sent']),
            models.Index(fields=['set', '-time_sent']),
        ]

    @property
    def percentage_done(self):
        if self.test is None:
            return 0
        return self.test * 100 // self.task.tests_count

    @property
    def language(self):
        return languages[self.language_id]

    def delete(self, using=None, keep_parents=False):
        if exists(self.directory):
            rmtree(self.directory)
        super().delete(using=using, keep_parents=keep_parents)

    @cached_property
    def files(self):
        data = []
        for file in SolutionFile.objects.filter(solution=self):
            try:
                text = file.text
            except:
                continue
            entity = {"filename": file.path, "text": text}
            end = file.path.split(".")[-1]
            language = None
            for l in languages:
                if l.file_type == end:
                    language = l
                    break
            if language is None:
                highlight = "nohighlight"
            else:
                highlight = "language-" + language.highlight
            entity["highlight"] = highlight
            data.append(entity)
        data.sort(key=lambda x: x["filename"])
        return data

    @property
    def directory(self):
        return "solutions/" + str(self.id)

    @property
    def number_result(self):
        if self.test is None:
            return self.result
        return f"{self.result} ({self.test})"

    @property
    def badge_style(self):
        if self.result == CONSTS["in_queue_status"]:
            return "secondary"
        if self.result == CONSTS["ok_status"]:
            return "success"
        if self.result == CONSTS["testing_status"]:
            return "info"
        return "danger"

    @property
    def testing_directory(self):
        return self.directory

    @property
    def volume_directory(self):
        return "/sprint-data/worker/" + str(self.id)

    def exec_command(self, command, working_directory="app", timeout=None):
        return call(
            f'docker exec -i solution_{self.id} sh -c "cd {working_directory} && {command}"',
            shell=True,
            timeout=timeout,
        )
