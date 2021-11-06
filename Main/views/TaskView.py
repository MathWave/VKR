from zipfile import ZipFile
from os.path import join

from Main.models import Solution, Progress
from SprintLib.BaseView import BaseView
from SprintLib.language import languages
from SprintLib.queue import send_testing
from SprintLib.testers import *


class TaskView(BaseView):
    required_login = True
    view_file = "task.html"

    def get(self):
        self.context['languages'] = sorted(languages, key=lambda x: x.name)
        progress, _ = Progress.objects.get_or_create(user=self.request.user, task=self.entities.task)
        self.context['progress'] = progress

    def pre_handle(self):
        if self.request.method == 'GET':
            return
        self.solution = Solution.objects.create(
            task=self.entities.task,
            user=self.request.user,
            language_id=int(self.request.POST["language"])
        )
        self.solution.create_dirs()

    def post_0(self):
        # отправка решения через текст
        filename = 'solution.' + self.solution.language.file_type
        file_path = join(self.solution.directory, filename)
        with open(file_path, 'w') as fs:
            fs.write(self.request.POST['code'])
        send_testing(self.solution.id)
        return "task?task_id=" + str(self.entities.task.id)

    def post_1(self):
        # отправка решения через файл
        if 'file' not in self.request.FILES:
            return "task?task_id=" + str(self.entities.task.id)
        filename = self.request.FILES['file'].name
        file_path = join(self.solution.directory, filename)
        with open(file_path, 'wb') as fs:
            for chunk in self.request.FILES['file'].chunks():
                fs.write(chunk)
        if filename.endswith('.zip'):
            with ZipFile(file_path) as obj:
                obj.extractall(self.solution.directory)
        send_testing(self.solution.id)
        return "task?task_id=" + str(self.entities.task.id)
