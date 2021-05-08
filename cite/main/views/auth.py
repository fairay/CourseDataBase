from .common import *


def login(request: ReqClass):
    msg = extract_msg(request)
    if check_account(request, bm.AllRoleCheck(), False) is not None:
        return render(request, 'main/login.html', locals())
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

