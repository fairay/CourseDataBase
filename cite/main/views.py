from django.shortcuts import render
from django.http import HttpResponse

import sys
sys.path.append("..")
from src import *
import model as bm  # cite.model


# Create your views here.
def home(request):
    # if request.method == 'POST':
    #     print(request.POST)

    acc_rep = inject.instance(AccountsRepository)
    user_list = [i.to_dict() for i in acc_rep.get_all()]
    for acc in acc_rep.get_all():
        print(acc)

    return render(request, 'main/login.html', locals())


def verify(request):
    acc = bm.AccountProc.login(request.POST['login'], request.POST['password'])
    if acc is not None:
        return HttpResponse("Авторизированно")
    else:
        return HttpResponse("Доступ отклонён")
