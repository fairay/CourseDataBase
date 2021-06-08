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
    proc = bm.AccountProc('admin')

    try:
        acc = proc.login(login_, password_)
    except exc.NotAuthorisedExc as e:
        request.session['warning_msg'] = 'Аккаунт не зарегистрирован'
        return HttpResponseRedirect(reverse('auth:login'))
    except exc.WrongPasswordExc as e:
        request.session['warning_msg'] = 'Авторизационные данные неверны, попробуйте снова'
        return HttpResponseRedirect(reverse('auth:login'))
    else:
        request.session['user'] = proc.get_cookie(acc.login)
        request.session['info_msg'] = 'Добро пожаловать!'
        return HttpResponseRedirect(reverse('users:profile'))


def verify(request: ReqClass):
    return authorize_user(request, request.POST['login'], request.POST['password'])


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


def upd_type(request: ReqClass):
    check_redirect = check_account(request, bm.BaseAccCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.AccountProc(request.session['user']['perstype'])
    try:
        request.session['user'] = proc.get_cookie(request.session['user']['login'])
    except exc.NoneExistExc as e:
        del request.session['user']
        request.session['warning_msg'] = 'Регистрация аккаунта была отклонена, попробуйте снова'
        return HttpResponseRedirect(reverse('auth:signup'))
    return HttpResponseRedirect(reverse('users:profile'))


def register(request: ReqClass):
    msg = extract_msg(request)
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('auth:login'))

    pre_data = extract_post(request)
    acc_proc = bm.AccountProc('admin')
    pers_proc = bm.PersonProc('admin')

    try:
        acc = acc_proc.create(**pre_data)
        acc_proc.register(acc)
    except exc.AlreadyExistsExc as e:
        request.session['warning_msg'] = 'Аккаунт с данным именем уже зарегистрирован, попробуйте другой логин'
        pre_data['login'] = ''
        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))
    except exc.CreateObjExc as e:
        request.session['warning_msg'] = 'Некорректный формат данных'
        if str(e) != '':
            request.session['warning_msg'] += ': ' + str(e)
        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))
    except exc.RepositoryExc as e:
        request.session['warning_msg'] = 'Аккаунт не был добавлен: ошибка работы базы данных'
        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))

    try:
        pers = pers_proc.create(**pre_data)
        pers_proc.add(pers)
    except exc.CreateObjExc as e:
        acc_proc.unregister(acc)
        request.session['warning_msg'] = 'Некорректные параметры дежурства'
        if str(e) != '':
            request.session['warning_msg'] = request.session['warning_msg'] + ': ' + str(e)

        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))

    except exc.RepositoryExc as e:
        acc_proc.unregister(acc)
        request.session['warning_msg'] = 'Ошибка регистрации личных данных'
        request.session['bad_signup'] = pre_data
        return HttpResponseRedirect(reverse('auth:signup'))

    return authorize_user(request, pre_data['login'], pre_data['password'])
