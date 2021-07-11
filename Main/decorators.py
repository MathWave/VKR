from django.http import HttpResponseRedirect


def login_required(boolean):
    def decorator(fun):
        def dec(request, *args, **kwargs):
            if request.user.is_authenticated != boolean:
                if boolean:
                    return HttpResponseRedirect('/enter')
                return HttpResponseRedirect('/main')
            return fun(request, *args, **kwargs)
        return dec
    return decorator
