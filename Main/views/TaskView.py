from zipfile import ZipFile

from Main.models import Solution
from Main.tasks import start_testing
from SprintLib.BaseView import BaseView, Language
from SprintLib.testers import *


class TaskView(BaseView):
    required_login = True
    view_file = "task.html"

    def get(self):
        self.context['languages'] = Language.objects.filter(opened=True).order_by('name')

    def pre_handle(self):
        if self.request.method == 'GET':
            return
        self.solution = Solution.objects.create(
            task=self.entities.task,
            user=self.request.user,
            language_id=self.request.POST["language"]
        )
        self.solution.create_dirs()

    def post_0(self):
        # отправка решения через текст
        filename = 'solution.' + self.solution.language.file_type
        file_path = join(self.solution.directory, filename)
        with open(file_path, 'w') as fs:
            fs.write(self.request.POST['code'])
        start_testing.delay(self.solution.id)
        return "task?task_id=" + str(self.entities.task.id)

    def post_1(self):
        # отправка решения через файл
        filename = self.request.FILES['file'].name
        file_path = join(self.solution.directory, filename)
        with open(file_path, 'wb') as fs:
            for chunk in self.request.FILES['file'].chunks():
                fs.write(chunk)
        if filename.endswith('.zip'):
            with ZipFile(file_path) as obj:
                obj.extractall(self.solution.directory)
        start_testing.delay(self.solution.id)
        return "task?task_id=" + str(self.entities.task.id)
