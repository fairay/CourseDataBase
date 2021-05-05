from django.shortcuts import render
from django.http import HttpResponse

import sys
sys.path.append("..") # Adds higher directory to python modules path.
# import src as s
from src import *


# Create your views here.
def home(request):
    if request.method == 'POST':
        print(request.POST)

    acc_rep = inject.instance(AccountsRepository)
    user_list = [i.to_dict() for i in acc_rep.get_all()]
    for acc in acc_rep.get_all():
        print(acc)

    return render(request, 'main/login.html', locals())


def verify(request):
    if request.method == 'POST':
        print(request.POST)

    return HttpResponse("Запрос верификации")
