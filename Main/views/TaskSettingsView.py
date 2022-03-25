from django.http import HttpResponse
from django.utils import timezone

from Main.models import ExtraFile, Dump, Task
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.queue import send_to_queue


class TaskSettingsView(BaseView):
    view_file = "task_settings.html"
    required_login = True
    endpoint = "admin/task"
    task: Task

    def pre_handle(self):
        if self.request.user != self.task.creator and self.request.user.username not in self.task.editors:
            raise AccessError()

    def get(self):
        self.context["error_message"] = self.request.GET.get("error_message", "")

    def post(self):
        for key, value in self.request.POST.items():
            setattr(self.task, key, value.strip())
        self.task.public = "public" in self.request.POST
        self.task.changes.append({
            'username': self.request.user.username,
            'action': 'Отредактировал условия',
            'time': timezone.now().strftime("%d-%m-%Y %H:%M:%s")
        })
        self.task.save()
        return f"/admin/task?task_id={self.task.id}"

    def post_dump(self):
        dump = Dump.objects.create(executor=self.request.user, task=self.task)
        send_to_queue("files", {"id": dump.id})
        return f"/admin/task?task_id={self.task.id}"

    def _upload(self, is_test):
        filename = self.request.FILES["file"].name
        ef, created = None, None
        if is_test:
            name = filename.strip(".a")
            if not name.isnumeric():
                return f"/admin/task?task_id={self.task.id}&error_message=Формат файла не соответствует тесту"
            ef, created = ExtraFile.objects.get_or_create(
                task=self.task, is_test=True, filename=filename
            )
            if not created:
                ef.is_sample = False
                ef.save()
                return f"/admin/task?task_id={self.task.id}"
        if ef is None or created is None:
            ef, created = ExtraFile.objects.get_or_create(
                task=self.task, filename=filename, is_test=is_test
            )
        ef.write(self.request.FILES["file"].read())
        try:
            var = ef.text
            ef.readable = True
        except UnicodeDecodeError:
            ef.readable = False
        ef.save()
        self.task.changes.append({
            'username': self.request.user.username,
            'action': f'Загрузил файл {filename}',
            'time': timezone.now().strftime("%d-%m-%Y %H:%M:%s")
        })
        self.task.save()
        return "/admin/task?task_id=" + str(self.task.id)

    def post_file_upload(self):
        return self._upload(False)

    def post_test_upload(self):
        return self._upload(True)

    def post_delete_file(self):
        ef = ExtraFile.objects.get(id=self.request.POST["id"])
        ef.delete()
        self.task.changes.append({
            'username': self.request.user.username,
            'action': f'Удалил файл {ef.filename}',
            'time': timezone.now().strftime("%d-%m-%Y %H:%M:%s")
        })
        self.task.save()
        return HttpResponse("ok")

    def _create(self, is_test):
        name = self.request.POST["newfile_name"]

        ef, created = ExtraFile.objects.get_or_create(
            filename=name, task=self.task
        )
        if not created:
            return f"/admin/task?task_id={self.task.id}&error_message=Файл с таким именем уже существует"
        ef.write(b"")
        ef.is_test = is_test
        ef.readable = True
        ef.save()
        self.task.changes.append({
            'username': self.request.user.username,
            'action': f'Создал файл {ef.filename}',
            'time': timezone.now().strftime("%d-%m-%Y %H:%M:%s")
        })
        self.task.save()
        return f"/admin/task?task_id={self.task.id}"

    def post_create_file(self):
        return self._create(False)

    def post_create_test(self):
        return self._create(True)

    def post_save_test(self):
        ef = ExtraFile.objects.get(id=self.request.POST["test_id"])
        ef.remove_from_fs()
        ef.write(self.request.POST["text"].encode("utf-8"))
        ef.is_sample = "is_sample" in self.request.POST.keys()
        ef.save()
        self.task.changes.append({
            'username': self.request.user.username,
            'action': f'Отредактировал файл {ef.filename}',
            'time': timezone.now().strftime("%d-%m-%Y %H:%M:%s")
        })
        self.task.save()
        return f"/admin/task?task_id={self.task.id}"

    def post_users_edit(self):
        current_users = self.task.editors
        for key, value in self.request.POST.items():
            if key.startswith("user_"):
                i = '_'.join(key.split("_")[1:])
                if i not in current_users:
                    self.task.editors.append(i)
        to_delete = [i for i in current_users if "user_" + i not in self.request.POST and i != self.request.user.username]
        for t in to_delete:
            self.task.editors.remove(t)
        self.task.changes.append({
            'username': self.request.user.username,
            'action': f'Изменил список редакторов',
            'time': timezone.now().strftime("%d-%m-%Y %H:%M:%s")
        })
        self.task.save()
        return "/admin/task?task_id=" + str(self.task.id)
