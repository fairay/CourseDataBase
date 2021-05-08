from .common import *


def my_profile(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AllRoleCheck())
    if check_redirect is not None:
        return check_redirect

    person = bm.PersonProc.profile_info(request.session['user']['login'])
    return render(request, 'auth/profile.html', locals())


def profile(request: ReqClass, login: str):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    if login == request.session['user']['login']:
        return HttpResponseRedirect(reverse('users:profile'))

    person = bm.PersonProc.profile_info(login)
    return render(request, 'auth/profile.html', locals())


def get_all(request: ReqClass):
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    person_arr = bm.PersonProc.all_profiles()
    return render(request, 'users/all.html', locals())
