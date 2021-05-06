from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest as ReqClass

from inject_config import *
import model as bm
import errors as exc


def check_account(request: ReqClass, verifier: bm.BaseAccCheck) -> HttpResponseRedirect:
    try:
        verifier.check(request.session)
    except exc.NotAuthorisedExc:
        print('@@@')
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
        return HttpResponseRedirect(reverse('auth:profile'))


def verify(request: ReqClass):
    acc = bm.AccountProc.login(request.POST['login'], request.POST['password'])

    if acc is not None:
        request.session['login'] = acc.get_login()
        request.session['perstype'] = acc.get_pers_type()

        return HttpResponseRedirect(reverse('auth:profile'))
    else:
        # TODO: Access denied message at login page
        return HttpResponseRedirect(reverse('auth:login'))


def profile(request: ReqClass):
    check_redirect = check_account(request, bm.AllRoleCheck())
    if check_redirect is not None:
        return check_redirect

    person = bm.PersonProc.profile_info(request.session['login'])
    perstype = bm.AccountProc.type_name(request.session['perstype'])

    return render(request, 'main/profile.html', locals())
