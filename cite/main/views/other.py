from .common import *


def trucks(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.DriverCheck())
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
    check_redirect = check_account(request, bm.GuardCheck())
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


def delivery(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.DriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DeliveryProc(request.session['user']['perstype'])
    del_arr = proc.get_all()
    return render(request, 'other/delivery.html', locals())


def add_delivery(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DeliveryProc(request.session['user']['perstype'])
    pre_data = extract_post(request)

    try:
        order = proc.create(**pre_data)
    except exc.DeliveryExc as ex:
        request.session['warning_msg'] = 'Некорректные параметры заказа'
        return HttpResponseRedirect(reverse('other:delivery'))

    order = proc.add(order)
    if order is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('other:delivery'))

    return HttpResponseRedirect(reverse('other:delivery'))


def delivery_page(request: ReqClass, orderid: int):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.DriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DeliveryProc(request.session['user']['perstype'])
    order = proc.delivery_info(orderid)
    return render(request, 'other/delivery_page.html', locals())


def assign_delivery(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.DriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DeliveryProc(request.session['user']['perstype'])
    pre_data = extract_post(request)

    try:
        proc.assign(pre_data['orderid'], pre_data['login'])
    except exc.WrongFormatExc as e:
        request.session['warning_msg'] = 'Некорректные параметры назначения заказа: ' + str(e)
    except exc.NoneExistExc as e:
        request.session['warning_msg'] = 'Данный заказ не существует'
        return HttpResponseRedirect(reverse('users:profile'))
    except exc.AlreadyPickedExc as e:
        request.session['warning_msg'] = 'Данный заказ уже назначен или доставлен'
    except exc.RepositoryExc:
        request.session['warning_msg'] = 'Объект не был обновлён: Ошибка в работе базы данных'
    else:
        request.session['info_msg'] = 'Заказ назначен водителю ' + pre_data['login']

    return HttpResponseRedirect(reverse('other:delivery_page', kwargs={'orderid': pre_data['orderid']}))


def pick_delivey(request: ReqClass, orderid: int):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.OnlyDriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DeliveryProc(request.session['user']['perstype'])

    try:
        proc.assign(orderid, request.session['user']['login'])
    except exc.WrongFormatExc as e:
        request.session['warning_msg'] = 'Некорректные параметры назначения заказа: ' + str(e)
    except exc.NoneExistExc as e:
        request.session['warning_msg'] = 'Данный заказ не существует'
        return HttpResponseRedirect(reverse('users:profile'))
    except exc.AlreadyPickedExc as e:
        request.session['warning_msg'] = 'Данный заказ уже назначен или доставлен'
    except exc.RepositoryExc:
        request.session['warning_msg'] = 'Объект не был обновлён: Ошибка в работе базы данных'
    else:
        request.session['info_msg'] = 'Заказ успешно назначен Вам'

    return HttpResponseRedirect(reverse('other:delivery_page', kwargs={'orderid': orderid}))


def done_delivery(request: ReqClass, orderid: int):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.DriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.DeliveryProc(request.session['user']['perstype'])
    try:
        proc.set_done(orderid, request.session['user']['login'])
    except exc.NoneExistExc as e:
        request.session['warning_msg'] = 'Данный заказ не существует'
        return HttpResponseRedirect(reverse('users:profile'))
    except exc.WrongFormatExc as e:
        request.session['warning_msg'] = 'Некорректные параметры: ' + str(e)
    except exc.NotAssignedExc as e:
        request.session['warning_msg'] = 'Заказ не в доставке'
    except exc.NotOnDutyExc as e:
        request.session['warning_msg'] = 'Заказ можно доставить только во время дежурства'
    except exc.RepositoryExc:
        request.session['warning_msg'] = 'Объект не был обновлён: Ошибка в работе базы данных'
    else:
        request.session['info_msg'] = 'Доставка зарегистрирована'

    return HttpResponseRedirect(reverse('other:delivery_page', kwargs={'orderid': orderid}))


def pass_record(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.AdminCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PassRecordProc(request.session['user']['perstype'])
    # pass_arr = proc.get_all()
    pass_arr = proc.get_with_login()

    truck_arr = bm.TruckProc(request.session['user']['perstype']).get_all()
    check_arr = bm.CheckpointProc(request.session['user']['perstype']).get_all()
    return render(request, 'other/pass_records.html', locals())


def driver_pass_record(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.OnlyDriverCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PassRecordProc(request.session['user']['perstype'])
    pass_arr = proc.get_by_login(request.session['user']['login'])
    return render(request, 'other/driver_passage.html', locals())


def guard_pass_record(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.OnlyGuardCheck())
    if check_redirect is not None:
        return check_redirect

    duty_proc = bm.GuardDutyProc(request.session['user']['perstype'])
    duty = duty_proc.get_current(request.session['user']['login'])
    if len(duty):
        duty = duty[0]
        proc = bm.PassRecordProc(request.session['user']['perstype'])
        pass_arr = proc.get_by_duty(duty)

        truck_arr = bm.TruckProc(request.session['user']['perstype']).get_all()
    else:
        duty = None
    return render(request, 'other/guard_passage.html', locals())


def add_pass_record(request: ReqClass):
    msg = extract_msg(request)
    check_redirect = check_account(request, bm.GuardCheck())
    if check_redirect is not None:
        return check_redirect

    proc = bm.PassRecordProc(request.session['user']['perstype'])
    pre_data = extract_post(request)

    try:
        record = proc.create(**pre_data)
    except exc.CreateObjExc as ex:
        request.session['warning_msg'] = 'Некорректные параметры записи проезда'
        return HttpResponseRedirect(reverse('other:pass_record'))

    record = proc.add(record)
    if record is None:
        request.session['warning_msg'] = 'Объект не был добавлен: Ошибка в работе базы данных'
        return HttpResponseRedirect(reverse('other:pass_record'))

    if request.session['user']['perstype'] == 'admin':
        return HttpResponseRedirect(reverse('other:pass_record'))
    else:
        return HttpResponseRedirect(reverse('other:guard_pass_record'))
