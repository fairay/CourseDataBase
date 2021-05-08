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


def authorize_user(request: ReqClass, login_: str, password_: str):
    acc = bm.AccountProc.login(login_, password_)

    if acc is not None:
        request.session['user'] = bm.AccountProc.get_cookie(acc)
        request.session['info_msg'] = 'Добро пожаловать!'
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        request.session['warning_msg'] = 'Авторизационные данные неверны, попробуйте снова'
        return HttpResponseRedirect(reverse('auth:login'))


def verify(request: ReqClass):
    return authorize_user(request, request.POST['login'], request.POST['password'])

    """
    acc = bm.AccountProc.login(request.POST['login'], request.POST['password'])

    if acc is not None:
        request.session['user'] = bm.AccountProc.get_cookie(acc)
        request.session['info_msg'] = 'Добро пожаловать!'
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        request.session['warning_msg'] = 'Авторизационные данные неверны, попробуйте снова'
        return HttpResponseRedirect(reverse('auth:login'))
    """


def signup(request: ReqClass):
    msg = extract_msg(request)

    # if request.method == 'POST':
    if "bad_signup" in request.session:
        pre_data = request.session['bad_signup']
        del request.session['bad_signup']

    if check_account(request, bm.AllRoleCheck(), False) is None:
        request.session['info_msg'] = 'Для прохождения регистрации выйдете из аккаунта'
        return HttpResponseRedirect(reverse('users:profile'))

    pers_types = bm.AccountProc.get_type_names()
    return render(request, 'auth/signup.html', locals())


def register(request: ReqClass):
    msg = extract_msg(request)
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('auth:login'))

    pre_data = dict(request.POST.copy())
    for key in pre_data.keys():
        pre_data[key] = pre_data[key][0]

    # TODO: verification data on account creation
    acc = bm.AccountProc.register(pre_data['login'], pre_data['password'], pre_data['perstype'])
    if acc is None:
        request.session['warning_msg'] = 'Аккаунт с данным именем уже зарегестрирован, попробуйте другой логин'
        pre_data['login'] = ''
        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))

    pers = bm.Person(**pre_data)
    pers = bm.PersonProc.register(pers)
    if pers is None:
        bm.AccountProc.unregister(acc)
        request.session['warning_msg'] = 'Ошибка регистрации личных данных'
        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))

    return authorize_user(request, pre_data['login'], pre_data['password'])
