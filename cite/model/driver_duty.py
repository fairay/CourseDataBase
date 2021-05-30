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

        if 'no_end' in init_dict.keys():
            init_dict['enddate'] = None

        init_dict['dutyid'] = None
        return DriverDuty(**init_dict)

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
