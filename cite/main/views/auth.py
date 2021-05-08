from .common import *
import requests


def login(request: ReqClass):
    msg = extract_msg(request)
    if check_account(request, bm.AllRoleCheck(), False) is not None:
        return render(request, 'auth/login.html', locals())
    else:
        return HttpResponseRedirect(reverse('users:profile'))


def logout(request: ReqClass):
    if 'user' in request.session:
        del request.session['user']
    return HttpResponseRedirect(reverse('auth:login'))


def verify(request: ReqClass):
    acc = bm.AccountProc.login(request.POST['login'], request.POST['password'])

    if acc is not None:
        request.session['user'] = bm.AccountProc.get_cookie(acc)
        request.session['info_msg'] = 'Добро пожаловать!'
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        request.session['warning_msg'] = 'Авторизационные данные неверны, попробуйте снова'
        return HttpResponseRedirect(reverse('auth:login'))


def signup(request: ReqClass):
    if request.method == 'POST':
        pre_data = request.POST

    if check_account(request, bm.AllRoleCheck(), False) is None:
        request.session['info_msg'] = 'Для прохождения регистрации выйдете из аккаунта'
        return HttpResponseRedirect(reverse('users:profile'))

    pers_types = bm.AccountProc.get_type_names()
    return render(request, 'auth/signup.html', locals())


def register(request: ReqClass):
    pass
