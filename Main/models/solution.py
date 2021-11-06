from os import mkdir, walk
from os.path import join, exists
from shutil import rmtree
from subprocess import call

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from Main.models.task import Task
from Sprint.settings import CONSTS, SOLUTIONS_ROOT, SOLUTIONS_ROOT_EXTERNAL
from SprintLib.language import languages


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language_id = models.IntegerField(default=0)
    time_sent = models.DateTimeField(default=timezone.now)
    result = models.TextField(default=CONSTS["in_queue_status"])

    @property
    def language(self):
        return languages[self.language_id]

    def delete(self, using=None, keep_parents=False):
        if exists(self.directory):
            rmtree(self.directory)
        super().delete(using=using, keep_parents=keep_parents)

    @property
    def files(self):
        data = []
        for path, _, files in walk(self.directory):
            if path.startswith(self.testing_directory):
                continue
            for file in files:
                try:
                    entity = {
                        'filename': file,
                        'text': open(join(path, file), 'r').read()
                    }
                    end = file.split('.')[-1]
                    language = None
                    for l in languages:
                        if l.file_type == end:
                            language = l
                            break
                    if language is None:
                        highlight = 'nohighlight'
                    else:
                        highlight = 'language-' + language.highlight
                    entity['highlight'] = highlight
                    data.append(entity)
                except:
                    continue
        data.sort(key=lambda x: x['filename'])
        return data

    def create_dirs(self):
        mkdir(self.directory)
        mkdir(self.testing_directory)

    @property
    def directory(self):
        return join(SOLUTIONS_ROOT, str(self.id))

    @property
    def testing_directory(self):
        return join(self.directory, 'test_dir')

    @property
    def volume_directory(self):
        return join(SOLUTIONS_ROOT_EXTERNAL, str(self.id), 'test_dir')

    def exec_command(self, command, working_directory='app', timeout=None):
        return call(f'docker exec -i solution_{self.id} sh -c "cd {working_directory} && {command}"', shell=True, timeout=timeout)
