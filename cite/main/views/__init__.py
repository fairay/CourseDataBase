from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest as ReqClass

import model as bm
import errors as exc
from inject_config import *

