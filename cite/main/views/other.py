from .common import *


def trucks(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.TruckProc(request.session['user']['perstype'])
    truck_arr = proc.get_all()
    return render(request, 'other/trucks.html', locals())


def add_truck(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.TruckProc(request.session['user']['perstype'])
    pre_data = extract_post(request)

    try:
        truck = proc.create(**pre_data)
    except exc.TruckExc as ex:
        request.session['warning_msg'] = 'Некорректные параметры машины'
        return HttpResponseRedirect(reverse('other:trucks'))

    truck = proc.add(truck)
    if truck is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('other:trucks'))

    return HttpResponseRedirect(reverse('other:trucks'))


def checkpoints(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.CheckpointProc(request.session['user']['perstype'])
    check_arr = proc.get_all()
    return render(request, 'other/check.html', locals())


def add_checkpoint(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.CheckpointProc(request.session['user']['perstype'])
    pre_data = extract_post(request)

    try:
        checkpoint = proc.create(**pre_data)
    except exc.TruckExc as ex:
        request.session['warning_msg'] = 'Некорректные параметры КПП'
        return HttpResponseRedirect(reverse('other:checkpoints'))

    checkpoint = proc.add(checkpoint)
    if checkpoint is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('other:checkpoints'))

    return HttpResponseRedirect(reverse('other:checkpoints'))
