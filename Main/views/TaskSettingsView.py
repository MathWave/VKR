from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from Main.models import ExtraFile
from SprintLib.BaseView import BaseView, AccessError


class TaskSettingsView(BaseView):
    view_file = "task_settings.html"
    required_login = True

    def pre_handle(self):
        if self.entities.task not in self.request.user.userinfo.available_tasks:
            raise AccessError()

    def get(self):
        self.context['error_message'] = self.request.GET.get('error_message', '')

    def post(self):
        for key, value in self.request.POST.items():
            setattr(self.entities.task, key, value.strip())
        self.entities.task.save()
        return f"/admin/task?task_id={self.entities.task.id}"

    def _upload(self, is_test):
        filename = self.request.FILES['file'].name
        ef, created = None, None
        if is_test:
            name = filename.strip('.a')
            if not name.isnumeric():
                return f'/admin/task?task_id={self.entities.task.id}&error_message=Формат файла не соответствует тесту'
            ef, created = ExtraFile.objects.get_or_create(task=self.entities.task, is_test=True, test_number=int(name))
            if not created:
                return f'/admin/task?task_id={self.entities.task.id}'
        if ef is None or created is None:
            ef, created = ExtraFile.objects.get_or_create(
                task=self.entities.task,
                filename=filename,
                is_test=is_test
            )
        with open(ef.path, 'wb') as fs:
            for chunk in self.request.FILES['file'].chunks():
                fs.write(chunk)
        try:
            open(ef.path, 'r').read()
            ef.readable = True
        except UnicodeDecodeError:
            ef.readable = False
        ef.save()
        return '/admin/task?task_id=' + str(self.entities.task.id)

    def post_file_upload(self):
        return self._upload(False)

    def post_test_upload(self):
        return self._upload(True)

    def post_delete_file(self):
        ef = ExtraFile.objects.get(id=self.request.POST['id'])
        ef.delete()
        return HttpResponse("ok")

    def _create(self, is_test):
        name = self.request.POST['newfile_name']

        ef, created = ExtraFile.objects.get_or_create(filename=name, task=self.entities.task)
        if not created:
            return f'/admin/task?task_id={self.entities.task.id}&error_message=Файл с таким именем уже существует'
        with open(ef.path, 'w') as fs:
            fs.write('')
        ef.is_test = is_test
        ef.readable = True
        ef.save()
        return f'/admin/task?task_id={self.entities.task.id}'

    def post_create_file(self):
        return self._create(False)

    def post_create_test(self):
        return self._create(True)
