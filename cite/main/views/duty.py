from .common import *


def drivers(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.DriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DriverDutyProc(request.session['user']['perstype'])
    duty_arr = proc.get_all()
    dow_names = proc.dow_short_names
    return render(request, 'duty/drivers.html', locals())


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

    print(duty)
    duty = proc.add(duty)
    if duty is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('duty:drivers'))

    return HttpResponseRedirect(reverse('duty:drivers'))
