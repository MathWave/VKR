import io
import json
from zipfile import ZipFile

from django.db import transaction

from Main.models import Task, ExtraFile
from SprintLib.BaseView import BaseView
from SprintLib.utils import write_bytes, delete_file


class TasksView(BaseView):
    view_file = "tasks.html"
    required_login = True
    endpoint = "tasks"

    def post(self):
        task_name = self.request.POST["name"]
        task = Task.objects.create(name=task_name, creator=self.request.user)
        return f"/admin/task?task_id={task.id}"

    def post_upload_file(self):
        archive = ZipFile(io.BytesIO(self.request.FILES["file"].read()))
        fs_ids = {}
        created = True
        try:
            with transaction.atomic():
                task = Task(name='новый таск', creator=self.request.user)
                for file in archive.infolist():
                    if file.filename == 'meta.json':
                        continue
                    else:
                        bts = archive.read(file.filename)
                        fs_id = write_bytes(bts)
                        readable = True
                        try:
                            bts.decode('utf-8')
                        except UnicodeDecodeError:
                            readable = False
                        fs_ids[file.filename] = fs_id, readable
                meta = json.loads(archive.read('meta.json').decode('utf-8'))
                task_fields = [
                    'name',
                    'public',
                    'legend',
                    'input_format',
                    'output_format',
                    'specifications',
                    'time_limit',
                    'time_estimation',
                ]
                for key in task_fields:
                    setattr(task, key, meta[key])
                task.save()
                for file in meta['files']:
                    fs_id, readable = fs_ids[str(file['id'])]
                    ExtraFile.objects.create(
                        filename=file['filename'],
                        is_test=file['is_test'],
                        is_sample=file['is_sample'],
                        fs_id=fs_id,
                        readable=readable,
                        task=task,
                    )
        except Exception as e:
            for fs_id in fs_ids.values():
                delete_file(fs_id[0])
            created = False
            raise e
        if created:
            return f"/admin/task?task_id={task.id}"
        return '/tasks'
