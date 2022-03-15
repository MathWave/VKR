import json
from os import mkdir, listdir, remove
from os.path import exists, join
from shutil import rmtree
from zipfile import ZipFile

from Main.models import Dump, ExtraFile
from SprintLib.queue import MessagingSupport
from SprintLib.utils import write_bytes


class Command(MessagingSupport):
    help = "starts file generator"
    queue_name = "files"

    def process_task(self, dump):
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
        task_data = {field: getattr(dump.task, field) for field in task_fields}
        files_fields = [
            'id',
            'filename',
            'is_test',
            'is_sample',
            'readable',
            'test_number'
        ]
        task_data['files'] = [
            {
                field: getattr(file, field)
                for field in files_fields
            }
            for file in ExtraFile.objects.filter(task=dump.task)
        ]
        tempdir = "/var/tmp/dump/"
        dump_filename = 'dump.zip'
        try:
            mkdir(tempdir)
            with open(join(tempdir, 'meta.json'), 'w') as fs:
                json.dump(task_data, fs)
            for ef in ExtraFile.objects.filter(task=dump.task):
                with open(join(tempdir, str(ef.id)), 'wb') as fs:
                    fs.write(ef.bytes)
            with ZipFile(dump_filename, 'w') as zipfile:
                for file in listdir(tempdir):
                    zipfile.write(join(tempdir, file))
            fs_id = write_bytes(open(dump_filename, 'rb').read())
            dump.fs_id = fs_id
            dump.save()
        finally:
            if exists(tempdir):
                rmtree(tempdir)
            if exists(dump_filename):
                remove(dump_filename)

    def process(self, payload: dict):
        id = payload['id']
        dump = Dump.objects.get(id=id)
        if dump.task:
            self.process_task(dump)
