import io
from zipfile import ZipFile

from Main.models import Solution, Progress, SolutionFile
from SprintLib.BaseView import BaseView
from SprintLib.language import languages
from SprintLib.queue import send_testing
from SprintLib.utils import write_bytes


class TaskView(BaseView):
    required_login = True
    view_file = "task.html"

    def get(self):
        progress, _ = Progress.objects.get_or_create(
            user=self.request.user, task=self.entities.task
        )
        self.context["progress"] = progress

    def pre_handle(self):
        if self.request.method == "GET":
            return
        self.solution = Solution.objects.create(
            task=self.entities.task,
            user=self.request.user,
            language_id=int(self.request.POST["language"]),
        )

    def post_0(self):
        # отправка решения через текст
        fs_id = write_bytes(self.request.POST["code"].encode("utf-8"))
        SolutionFile.objects.create(
            path="solution." + self.solution.language.file_type,
            solution=self.solution,
            fs_id=fs_id,
        )
        send_testing(self.solution.id)
        return "task?task_id=" + str(self.entities.task.id)

    def post_1(self):
        # отправка решения через файл
        if "file" not in self.request.FILES:
            return "task?task_id=" + str(self.entities.task.id)
        filename = self.request.FILES["file"].name
        if filename.endswith(".zip"):
            archive = ZipFile(io.BytesIO(self.request.FILES['file'].read()))
            for file in archive.infolist():
                if file.is_dir():
                    continue
                fs_id = write_bytes(archive.read(file.filename))
                SolutionFile.objects.create(
                    path=file.filename,
                    solution=self.solution,
                    fs_id=fs_id,
                )
        else:
            fs_id = write_bytes(self.request.FILES['file'].read())
            SolutionFile.objects.create(
                path=filename,
                solution=self.solution,
                fs_id=fs_id,
            )
        send_testing(self.solution.id)
        return "task?task_id=" + str(self.entities.task.id)
