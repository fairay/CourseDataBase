from inject_config import *
from .base_proc import BaseProc
from objects import *
import errors as exc
from .person_proc import PersonProc

import re
import datetime
import time


class DeliveryProc(BaseProc):
    order_dict = {'not_assigned': 0,
                  'in_transit': 1,
                  'delivered': 2,}
    rus_status = {'not_assigned': 'Не назначен',
                  'in_transit': 'В доставке',
                  'delivered': 'Доставлен',}

    @staticmethod
    def sort_delivery(arr: [Delivery]) -> [Delivery]:
        res = sorted(arr, key=lambda obj: obj.creation_t, reverse=True)
        return sorted(res, key=lambda obj: DeliveryProc.order_dict[obj.status])

    @staticmethod
    def create(**init_dict) -> Delivery:
        if not {'address', 'phonenumber'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        init_dict['phonenumber'] = DeliveryProc.transform_phone('+7 ' + init_dict['phonenumber'])
        if init_dict['phonenumber'] is None:
            raise exc.WrongFormatExc()
        init_dict['orderid'] = None
        init_dict['status'] = 'not_assigned'
        init_dict['creationtime'] = datetime.datetime.now()

        return Delivery(**init_dict)

    def get_all(self):
        rep_ = inject.instance(DeliveryRepository)(self._con)
        del_arr = []
        for obj in self.sort_delivery(rep_.get_all()):
            del_arr.append(self._to_view(obj))

        return del_arr

    def add(self, obj: Delivery):
        rep_ = inject.instance(DeliveryRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    def delivery_info(self, orderid: int) -> dict:
        rep_ = inject.instance(DeliveryRepository)(self._con)
        obj = rep_.get_by_id(orderid)
        if obj is None:
            return None
        return self._to_view(obj)

    def _to_view(self, obj: Delivery, extended=False) -> dict:
        d = obj.to_dict()
        d['rus_status'] = DeliveryProc.rus_status[d['status']]

        d['creationtime'] = d['creationtime'].strftime('%d.%m.%Y %H:%M:%S')
        if d['completiontime'] is not None:
            d['completiontime'] = d['creationtime'].strftime('%d.%m.%Y %H:%M:%S')
        if extended and d['login'] is not None:
            d['driver'] = PersonProc(self._con).profile_info(d['login'])

        return d
