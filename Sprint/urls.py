from django.contrib import admin
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

urlpatterns.append(path("admin/", admin.site.urls))
