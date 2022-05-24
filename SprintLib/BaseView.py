from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


class AccessError(Exception):
    pass


class BaseView:
    request: WSGIRequest = None
    context: Optional[dict] = None
    required_login: Optional[bool] = None
    view_file: Optional[str] = None
    endpoint: Optional[str] = None
    fields_except: tuple[str] = ()

    def __init__(self, request):
        self.context = {}
        self.request = request

    @classmethod
    def as_view(cls):
        @csrf_exempt
        def execute(request):
            if request.user.is_authenticated:
                user_info = request.user.userinfo
                user_info.last_request = timezone.now()
                user_info.save()
            c = cls(request)
            if c.required_login is not None:
                if c.required_login and not request.user.is_authenticated:
                    return HttpResponseRedirect("/enter")
                if c.required_login and not request.user.userinfo.verified:
                    return HttpResponseRedirect("/set_username")
                if (
                    not c.required_login
                    and request.user.is_authenticated
                    and request.user.userinfo.verified
                ):
                    return HttpResponseRedirect("/")
            request_method = request.method.lower()
            exec("from Main.models import *")
            context = {}
            for key in request.GET.keys():
                if key.endswith("_id") and key not in cls.fields_except:
                    model_name = key.rstrip("_id")
                    setattr(
                        c,
                        model_name,
                        eval(model_name[0].upper() + model_name[1:]).objects.get(
                            id=int(request.GET[key])
                        ),
                    )
                    context[model_name] = getattr(c, model_name)
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
                res = render(request, c.view_file, context)
                res.headers["X-Frame-Options"] = "ALLOW"
                return res
            except AccessError:
                return HttpResponseRedirect("/")

        return execute

    def pre_handle(self):
        pass

    def get(self):
        pass

    def post(self):
        pass
