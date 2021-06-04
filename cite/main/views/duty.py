from .common import *


def drivers(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DriverDutyProc(request.session['user']['perstype'])
    active_duty_arr = proc.get_current()
    duty_arr = proc.get_all()
    dow_names = proc.dow_short_names
    return render(request, 'duty/drivers.html', locals())


def my_drivers(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.OnlyDriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DriverDutyProc(request.session['user']['perstype'])
    duty_arr = proc.get_all(request.session['user']['login'])
    closest_duty = proc.get_closest(request.session['user']['login'])
    dow_names = proc.dow_short_names

    return render(request, 'duty/my_drivers.html', locals())


def add_driver_duty(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DriverDutyProc(request.session['user']['perstype'])
    pre_data = extract_post(request, listargs=['dow'])

    try:
        duty = proc.create(**pre_data)
    except exc.CreateObjExc as ex:
        request.session['warning_msg'] = 'Некорректные параметры дежурства'
        if str(ex) != '':
            request.session['warning_msg'] = request.session['warning_msg'] + ': ' + str(ex)
        return HttpResponseRedirect(reverse('duty:drivers'))

    duty = proc.add(duty)
    if duty is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('duty:drivers'))

    return HttpResponseRedirect(reverse('duty:drivers'))


def guards(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.GuardCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.GuardDutyProc(request.session['user']['perstype'])
    active_duty_arr = proc.get_current_view()
    duty_arr = proc.get_all()
    dow_names = proc.dow_short_names
    return render(request, 'duty/guards.html', locals())


def my_guards(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.OnlyGuardCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.GuardDutyProc(request.session['user']['perstype'])
    duty_arr = proc.get_all(request.session['user']['login'])
    closest_duty = proc.get_closest(request.session['user']['login'])
    dow_names = proc.dow_short_names

    return render(request, 'duty/my_guards.html', locals())


def add_guard_duty(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.GuardDutyProc(request.session['user']['perstype'])
    pre_data = extract_post(request, listargs=['dow'])

    try:
        duty = proc.create(**pre_data)
    except exc.CreateObjExc as ex:
        request.session['warning_msg'] = 'Некорректные параметры дежурства'
        if str(ex) != '':
            request.session['warning_msg'] = request.session['warning_msg'] + ': ' + str(ex)
        return HttpResponseRedirect(reverse('duty:guards'))

    duty = proc.add(duty)
    if duty is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('duty:guards'))

    return HttpResponseRedirect(reverse('duty:guards'))
