from django.http import HttpResponse

from SprintLib.BaseView import BaseView, AccessError
from SprintLib.utils import get_bytes


class DownloadFileView(BaseView):
    endpoint = "download_file"
    required_login = True

    def get(self):
        dump = self.entities.dump
        if dump.task:
            if self.request.user == dump.task.creator or self.request.user.username in dump.task.editors:
                response = HttpResponse(
                    get_bytes(dump.fs_id), content_type='application/force-download'
                )
                response['Content-Disposition'] = f'inline; filename={dump.filename}'
                return response
        raise AccessError()
