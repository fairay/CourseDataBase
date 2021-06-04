from .common import *


def _profile(request: ReqClass, login: str, msg=None):
    proc = bm.PersonProc(request.session['user']['perstype'])
    person = proc.profile_info(login)
    if person is None:
        request.session['warning_msg'] = 'Ошибка: профиль не найден'
        if login == request.session['user']['login']:
            return HttpResponseRedirect(reverse('auth:logout'))
        else:
            return HttpResponseRedirect(reverse('users:all'))

    if person['pers_type'] == 'driver':
        del_arr = bm.DeliveryProc(person['pers_type']).get_all(person['login'])
    return render(request, 'auth/profile.html', locals())


def my_profile(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.BaseAccCheck())
    if check_redirect is not None:
        return check_redirect

    return _profile(request, request.session['user']['login'], msg)


def profile(request: ReqClass, login: str):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    if login == request.session['user']['login']:
        return HttpResponseRedirect(reverse('users:profile'))

    return _profile(request, login, msg)


def get_all(request: ReqClass):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PersonProc(request.session['user']['perstype'])
    person_arr = proc.all_profiles(bm.AccountProc.verified)
    return render(request, 'users/all.html', locals())


def approve_user(request: ReqClass, login: str):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    msg = 'Ошибка операции подтверждения: '
    proc = bm.AccountProc(request.session['user']['perstype'])
    try:
        proc.approve(login)
    except exc.NonExistentExc:
        request.session['warning_msg'] = msg + 'аккаунт не зарегистрирован'
    except exc.VerifiedExc:
        request.session['warning_msg'] = msg + 'аккаунт уже подтверждён'
    except exc.RepositoryExc:
        request.session['warning_msg'] = msg + 'ошибка на сервере'
    else:
        request.session['info_msg'] = 'Аккаунт ' + ' успешно подтверждён'

    return get_unverified(request)


def del_user(request: ReqClass, login: str):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PersonProc(request.session['user']['perstype'])
    try:
        proc.delete(login)
    except exc.CreateObjExc as ex:
        request.session['warning_msg'] = 'Ошибка операции: ' + str(ex)

    return get_unverified(request)


def get_unverified(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PersonProc(request.session['user']['perstype'])
    person_arr = proc.all_profiles(bm.AccountProc.unverified, True)
    return render(request, 'users/unverified.html', locals())
