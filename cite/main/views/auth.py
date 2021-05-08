from .common import *


def login(request: ReqClass):
    msg = extract_msg(request)
    if check_account(request, bm.AllRoleCheck(), False) is not None:
        return render(request, 'main/login.html', locals())
    else:
        return HttpResponseRedirect(reverse('users:profile'))


def verify(request: ReqClass):
    acc = bm.AccountProc.login(request.POST['login'], request.POST['password'])

    if acc is not None:
        request.session['user'] = bm.AccountProc.get_cookie(acc)
        request.session['info_msg'] = 'Добро пожаловать!'
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        # TODO: Access denied message at login page
        return HttpResponseRedirect(reverse('auth:login'))

