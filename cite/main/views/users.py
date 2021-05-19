from .common import *


def my_profile(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.BaseAccCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PersonProc(request.session['user']['perstype'])
    person = proc.profile_info(request.session['user']['login'])
    if person is None:
        msg['warning'] = 'Ошибка: профиль не найден'
    return render(request, 'auth/profile.html', locals())


def profile(request: ReqClass, login: str):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    if login == request.session['user']['login']:
        return HttpResponseRedirect(reverse('users:profile'))

    proc = bm.PersonProc(request.session['user']['perstype'])
    person = proc.profile_info(login)
    return render(request, 'auth/profile.html', locals())


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
    try:
        bm.AccountProc.approve(login)
    except exc.NonExistentExc:
        request.session['warning_msg'] = msg + 'аккаунт не зарегистрирован'
    except exc.VerifiedExc:
        request.session['warning_msg'] = msg + 'аккаунт уже подтверждён'
    except exc.RepositoryExc:
        request.session['warning_msg'] = msg + 'ошибка на сервере'
    else:
        request.session['info_msg'] = 'Аккаунт ' + ' успешно подтверждён'

    return get_unverified(request)


def get_unverified(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PersonProc(request.session['user']['perstype'])
    person_arr = proc.all_profiles(bm.AccountProc.unverified, True)
    return render(request, 'users/unverified.html', locals())
