from django.shortcuts import render, redirect
from django.http import HttpResponse


def allowd_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("you are not authorized to view this page", status=403)

        return wrapper_func
    return decorator