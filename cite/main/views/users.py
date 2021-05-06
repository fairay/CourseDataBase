from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest as ReqClass

from inject_config import *
import model as bm
import errors as exc
from .auth import check_account


def my_profile(request: ReqClass):
    check_redirect = check_account(request, bm.AllRoleCheck())
    if check_redirect is not None:
        return check_redirect

    person = bm.PersonProc.profile_info(request.session['user']['login'])
    return render(request, 'main/profile.html', locals())


def profile(request: ReqClass, login: str):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    if login == request.session['user']['login']:
        return HttpResponseRedirect(reverse('users:profile'))

    person = bm.PersonProc.profile_info(login)
    return render(request, 'main/profile.html', locals())


# def get_all(request: ReqClass):
#     check_redirect = check_account(request, bm.AdminCheck())
#     if check_redirect is not None:
#         return check_redirect


