from inject_config import *
from .base_proc import BaseProc
from .acc_proc import AccountProc
from .truck_proc import TruckProc
from objects import *
import errors as exc

import re
from datetime import *


class DriverDutyProc(BaseProc):
    dow_short_names = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    dow_long_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

    def create(self, **init_dict) -> DriverDuty:
        if not {'platenumber', 'login', 'begindate', 'enddate', 'begintime',
                'endtime', 'dow'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        init_dict['begintime'] = datetime.strptime(init_dict['begintime'], '%H:%M').time()
        init_dict['endtime'] = datetime.strptime(init_dict['endtime'], '%H:%M').time()
        if init_dict['begintime'] >= init_dict['endtime']:
            raise exc.WrongFormatExc('время начала смены больше времени завершения')

        if not init_dict['dow']:
            raise exc.WrongFormatExc()
        init_dict['dow'] = self._dow_db(init_dict['dow'])

        if not AccountProc(con=self._con).check_role(init_dict['login'], 'driver'):
            raise exc.WrongFormatExc('аккаунт не пренадлежит водителю')
        if TruckProc(con=self._con).get(init_dict['platenumber']) is None:
            raise exc.NoneExistExc('машина не существует')

        init_dict['begindate'] = datetime.strptime(init_dict['begindate'], '%Y-%m-%d')
        init_dict['enddate'] = datetime.strptime(init_dict['enddate'], '%Y-%m-%d')

        if 'no_end' in init_dict.keys():
            init_dict['enddate'] = None
        elif init_dict['begindate'] > init_dict['enddate']:
            raise exc.WrongFormatExc('дата начала смены больше даты окончания')

        init_dict['dutyid'] = None
        duty = DriverDuty(**init_dict)

        if not self.is_driver_free(duty):
            raise exc.WrongFormatExc('водитель занят в данный период')
        if not self.is_truck_free(duty):
            raise exc.WrongFormatExc('машина занята в данный период')
        return duty

    def is_driver_free(self, obj: DriverDuty) -> bool:
        rep_: DriverDutyRepository = inject.instance(DriverDutyRepository)(self._con)
        for other in rep_.get_by_time(obj.bdate, obj.edate, login=obj.login):
            if self._is_collide(obj, other):
                return False
        return True

    def is_truck_free(self, obj: DriverDuty) -> bool:
        rep_: DriverDutyRepository = inject.instance(DriverDutyRepository)(self._con)
        for other in rep_.get_by_time(obj.bdate, obj.edate, platenumber=obj.number):
            print("Truck:", other)
            if self._is_collide(obj, other):
                return False
        return True

    def get_all(self):
        rep_ = inject.instance(DriverDutyRepository)(self._con)
        duty_arr = []
        for obj in rep_.get_all():
            duty_arr.append(self._to_view(obj))

        return duty_arr

    def add(self, obj: DriverDuty):
        rep_ = inject.instance(DriverDutyRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    def _to_view(self, obj: DriverDuty):
        d = obj.to_dict()
        d['begindate'] = d['begindate'].strftime('%d.%m.%Y')
        if d['enddate'] is not None:
            d['enddate'] = d['enddate'].strftime('%d.%m.%Y')

        d['dow_view'] = self._dow_view(d['dow'])
        d['begintime'] = d['begintime'].strftime('%H:%M')
        d['endtime'] = d['endtime'].strftime('%H:%M')
        return d

    def _dow_view(self, dow_str: str, short=False) -> dict:
        if short:
            title_arr = self.dow_short_names
        else:
            title_arr = self.dow_long_names

        dow_dict = {}
        for val in title_arr:
            dow_dict[val] = False

        for day in dow_str:
            dow_dict[title_arr[int(day)]] = True

        print(dow_dict)
        return dow_dict

    def _dow_db(self, dow_lst: [str]) -> str:
        ans_str = ''
        for i in range(len(self.dow_short_names)):
            if self.dow_short_names[i] in dow_lst:
                ans_str = ans_str + str(i)

        return ans_str

    @staticmethod
    def _is_collide(obj1: DriverDuty, obj2: DriverDuty):
        dow_inter = set(obj2.dow).intersection(obj1.dow)
        if not len(dow_inter):
            return False

        return (obj2.btime <= obj1.btime <= obj2.etime or
                obj1.btime <= obj2.btime <= obj1.etime)
