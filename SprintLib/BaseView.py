from typing import Optional

from django.db import transaction
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from SprintLib.EntityStorage import EntityStorage


class AccessError(Exception):
    pass


class BaseView:
    request: WSGIRequest = None
    context: dict = {}
    entities = EntityStorage()
    required_login: Optional[bool] = None
    view_file: Optional[str] = None

    @classmethod
    def as_view(cls):
        @transaction.atomic
        def execute(request):
            if request.user.is_authenticated:
                user_info = request.user.userinfo
                user_info.last_request = timezone.now()
                user_info.save()
            c = cls()
            if c.required_login is not None:
                if c.required_login and not request.user.is_authenticated:
                    return HttpResponseRedirect("/enter")
                if not c.required_login and request.user.is_authenticated:
                    return HttpResponseRedirect("/")
            request_method = request.method.lower()
            c.request = request
            exec("from Main.models import *")
            for key in request.GET.keys():
                if key.endswith("_id"):
                    model_name = key.rstrip("_id")
                    c.entities.add(
                        model_name,
                        eval(model_name.capitalize()).objects.get(
                            id=int(request.GET[key])
                        ),
                    )
            context = c.entities.entities
            if "action" in request.POST.keys():
                request_method += "_" + request.POST["action"]
            method = getattr(c, request_method, None)
            try:
                data = c.pre_handle()
                if method:
                    if data is None:
                        data = method()
                    if type(data) == str:
                        return HttpResponseRedirect(data)
                    if type(data) == dict:
                        return JsonResponse(data)
                    if data is not None:
                        return data
                context = {**context, **c.context}
                return render(request, c.view_file, context)
            except AccessError:
                return HttpResponseRedirect("/")

        return execute

    def pre_handle(self):
        pass

    def get(self):
        pass

    def post(self):
        pass
