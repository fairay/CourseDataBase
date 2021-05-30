from . import *


def check_account(request: ReqClass, verifier: bm.BaseAccCheck, set_msg=True) -> HttpResponseRedirect or None:
    if 'user' not in request.session.keys():
        if set_msg:
            request.session['warning_msg'] = 'Авторизируйтесь для доступа к сайту'
        return HttpResponseRedirect(reverse('auth:login'))

    try:
        verifier.check(request.session['user'])

    except exc.NotAuthorisedExc:
        if set_msg:
            request.session['warning_msg'] = 'Авторизируйтесь для доступа к сайту'
        return HttpResponseRedirect(reverse('auth:login'))

    except exc.UnverifiedExc:
        if set_msg:
            request.session['info_msg'] = 'Функция недоступна :' \
                                          'Ваша регистрация не подтверждена администратором.'
        return HttpResponseRedirect(reverse('users:profile'))

    except exc.NotAllowedExc:
        if set_msg:
            request.session['warning_msg'] = 'Данная функция недоступна вашму аккаунту'
        return HttpResponseRedirect(reverse('auth:login'))

    return None


def extract_msg(request: ReqClass) -> dict:
    msg = {}

    if 'warning_msg' in request.session:
        msg["warning"] = request.session['warning_msg']
        del request.session['warning_msg']

    elif 'info_msg' in request.session:
        msg["info"] = request.session['info_msg']
        del request.session['info_msg']

    return msg


def extract_post(request: ReqClass, listargs=[]) -> dict:
    data = dict(request.POST)
    for key in data.keys():
        data[key] = data[key][0]

    for lst in listargs:
        data[lst] = request.POST.getlist(lst)

    return data
