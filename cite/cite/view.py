from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest as ReqClass

from main.views.common import extract_msg


def unknown_error(request: ReqClass):
    msg = extract_msg(request)
    return render(request, 'unknown_error.html', locals())
