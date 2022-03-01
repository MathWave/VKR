from os.path import join

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

import Main.views
from Main.views import *


urlpatterns = [
    path("checker/", include("Checker.urls")),
    path("messaging/", include("Messaging.urls")),
]

for v in dir(Main.views):
    try:
        view = eval(v)
    except NameError:
        continue
    if hasattr(view, 'endpoint') and view.endpoint is not None:
        urlpatterns.append(path(view.endpoint, view.as_view()))


def csr(request, file_path):
    response = HttpResponse(open(join("certs", file_path.lower()), 'rb').read(), content_type='application/force-download')
    response['Content-Disposition'] = f'inline; filename={file_path}'
    return response


urlpatterns.append(path('.well-known/pki-validation/<str:file_path>', csr))
urlpatterns.append(path("admin/", admin.site.urls))
