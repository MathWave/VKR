from django.http import HttpResponse

from Main.models import Dump
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.utils import get_bytes


class DownloadFileView(BaseView):
    endpoint = "download_file"
    required_login = True
    dump: Dump

    def get(self):
        if self.dump.task:
            if self.request.user == self.dump.task.creator or self.request.user.username in self.dump.task.editors:
                response = HttpResponse(
                    get_bytes(self.dump.fs_id), content_type='application/force-download'
                )
                response['Content-Disposition'] = f'inline; filename={self.dump.filename}'
                return response
        raise AccessError()
