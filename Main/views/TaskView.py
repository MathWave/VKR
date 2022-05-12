import io
from typing import Optional
from zipfile import ZipFile

from Main.models import Solution, Progress, SolutionFile, SetTask, Task, Set
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.language import languages
from SprintLib.utils import write_bytes, send_testing


class TaskView(BaseView):
    required_login = True
    view_file = "task.html"
    endpoint = "task"
    setTask: Optional[SetTask] = None
    task: Optional[Task] = None
    set: Optional[Set] = None

    def get(self):
        progress, _ = Progress.objects.get_or_create(
            user=self.request.user, task=self.task
        )
        self.context["progress"] = progress
        self.context["in_set"] = self.set is not None

    def pre_handle(self):
        if self.setTask:
            self.set = self.setTask.set
            self.task = self.setTask.task
            self.context['set'] = self.set
            self.context['task'] = self.task
            self.context['languages'] = self.set.language_models
        else:
            if not self.task.public and self.task.creator != self.request.user and self.request.user.username not in self.task.editors:
                raise AccessError()
            self.context['languages'] = languages
        if self.request.method == "GET":
            return
        if self.set and int(self.request.POST["language"]) not in self.set.languages:
            raise AccessError()
        self.solution = Solution.objects.create(
            task=self.task,
            user=self.request.user,
            language_id=int(self.request.POST["language"]),
            set=self.set,
            extras=dict(),
        )

    def post_0(self):
        # отправка решения через текст
        fs_id = write_bytes(self.request.POST["code"].encode("utf-8"))
        SolutionFile.objects.create(
            path="solution." + self.solution.language.file_type,
            solution=self.solution,
            fs_id=fs_id,
        )
        send_testing(self.solution)
        return ("/task?setTask_id=" + str(self.setTask.id)) if self.set else ("/task?task_id=" + str(self.task.id))

    def post_1(self):
        # отправка решения через файл
        if "file" not in self.request.FILES:
            return "task?task_id=" + str(self.task.id)
        filename = self.request.FILES["file"].name
        if filename.endswith(".zip"):
            archive = ZipFile(io.BytesIO(self.request.FILES["file"].read()))
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
            fs_id = write_bytes(self.request.FILES["file"].read())
            SolutionFile.objects.create(
                path=filename,
                solution=self.solution,
                fs_id=fs_id,
            )
        send_testing(self.solution)
        return ("/task?setTask_id=" + str(self.setTask.id)) if self.set else ("/task?task_id=" + str(self.task.id))
