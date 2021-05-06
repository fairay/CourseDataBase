from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest as ReqClass

from inject_config import *
import model as bm
import errors as exc


def check_account(request: ReqClass, verifier: bm.BaseAccCheck) -> HttpResponseRedirect or None:
    if 'user' not in request.session.keys():
        return HttpResponseRedirect(reverse('auth:login'))

    try:
        verifier.check(request.session['user'])
    except exc.NotAuthorisedExc:
        return HttpResponseRedirect(reverse('auth:login'))
    except exc.UnverifiedExc:
        return HttpResponseRedirect(reverse('auth:login'))
    except exc.NotAllowedExc:
        return HttpResponseRedirect(reverse('auth:login'))

    return None


def login(request: ReqClass):
    if check_account(request, bm.AllRoleCheck()) is not None:
        return render(request, 'main/login.html', locals())
    else:
        return HttpResponseRedirect(reverse('users:profile'))


def verify(request: ReqClass):
    acc = bm.AccountProc.login(request.POST['login'], request.POST['password'])

    if acc is not None:
        request.session['user'] = bm.AccountProc.get_cookie(acc)
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        # TODO: Access denied message at login page
        return HttpResponseRedirect(reverse('auth:login'))

