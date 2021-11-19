from django.http import HttpResponse

from SprintLib.BaseView import BaseView
from SprintLib.utils import get_bytes


class ImageView(BaseView):
    def get(self):
        return HttpResponse(get_bytes(int(self.request.GET['id'])), content_type="image/jpg")
