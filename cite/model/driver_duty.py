from inject_config import *
from .base_proc import BaseProc
from .acc_proc import AccountProc
from .truck_proc import TruckProc
from .base_duty import BaseDutyProc
from objects import *
import errors as exc

import re
from datetime import *


class DriverDutyProc(BaseDutyProc):
    def create(self, **init_dict) -> DriverRDuty:
        if not {'platenumber', 'login', 'begindate', 'enddate', 'begintime',
                'endtime', 'dow'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        init_dict = self._pre_create(**init_dict)

        if not AccountProc(con=self._con).check_role(init_dict['login'], 'driver'):
            raise exc.WrongFormatExc('аккаунт не пренадлежит водителю')
        if TruckProc(con=self._con).get(init_dict['platenumber']) is None:
            raise exc.NoneExistExc('машина не существует')

        init_dict['dutyid'] = None
        init_dict['ruleid'] = None
        duty = DriverRDuty(**init_dict)

        if not self.is_driver_free(duty):
            raise exc.WrongFormatExc('водитель занят в данный период')
        if not self.is_truck_free(duty):
            raise exc.WrongFormatExc('машина занята в данный период')
        return duty

    def is_driver_free(self, obj: DriverRDuty) -> bool:
        rep_: DriverRDutyRepository = inject.instance(DriverRDutyRepository)(self._con)
        for other in rep_.get_by_time(obj.bdate, obj.edate, login=obj.login):
            if self._is_collide(obj, other):
                return False
        return True

    def is_truck_free(self, obj: DriverRDuty) -> bool:
        rep_: DriverRDutyRepository = inject.instance(DriverRDutyRepository)(self._con)
        for other in rep_.get_by_time(obj.bdate, obj.edate, platenumber=obj.number):
            if self._is_collide(obj, other):
                return False
        return True

    def get_all(self, login: str = None):
        rep_ = inject.instance(DriverRDutyRepository)(self._con)
        duty_arr = []

        for obj in rep_.get_all():
            if login is None or obj.login == login:
                duty_arr.append(self._to_view(obj))

        return duty_arr

    def get_current(self, login: str = None, platenumber: str = None):
        return self.get_by_time(datetime.now(), login, platenumber)
        # rep_: DriverDutyRepository = inject.instance(DriverDutyRepository)(self._con)
        # duty_arr = []
        # now_date = datetime.now().date()
        # for obj in rep_.get_by_time(now_date, now_date):
        #     if self._is_active(obj, datetime.now()):
        #         duty_arr.append(self._to_view(obj))
        #
        # return duty_arr

    def get_by_time(self, date_time, login: str = None, platenumber: str = None):
        rep_: DriverRDutyRepository = inject.instance(DriverRDutyRepository)(self._con)
        duty_arr = []
        date_ = date_time.date()
        for obj in rep_.get_by_time(date_, date_, login, platenumber):
            if self._is_active(obj, date_time):
                duty_arr.append(self._to_view(obj))

        return duty_arr

    def get_closest(self, login: str):
        rep_: DriverRDutyRepository = inject.instance(DriverRDutyRepository)(self._con)

        date_ = datetime.now().date()
        duty_arr = rep_.get_by_time(date_, None, login)

        if len(duty_arr) == 0:
            return None

        min_duty = duty_arr[0]
        min_date = self._closest_date(datetime.now(), min_duty)

        for obj in duty_arr:
            cl_date = self._closest_date(datetime.now(), obj)
            if min_date > cl_date or (min_date == cl_date and min_duty.btime > obj.btime):
                min_date = cl_date
                min_duty = obj

        min_duty = self._to_view(min_duty)
        min_duty['min_date'] = min_date.strftime('%d.%m.%Y')
        return min_duty

    def add(self, obj: DriverRDuty):
        rep_ = inject.instance(DriverRDutyRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    def _to_view(self, obj: DriverRDuty):
        d = obj.to_dict()
        d['begindate'] = d['begindate'].strftime('%d.%m.%Y')
        if d['enddate'] is not None:
            d['enddate'] = d['enddate'].strftime('%d.%m.%Y')

        d['dow_view'] = self._dow_view(d['dow'])
        d['begintime'] = d['begintime'].strftime('%H:%M')
        d['endtime'] = d['endtime'].strftime('%H:%M')
        return d

    @staticmethod
    def _is_collide(obj1: DriverRDuty, obj2: DriverRDuty):
        dow_inter = set(obj2.dow).intersection(obj1.dow)
        if not len(dow_inter):
            return False

        return (obj2.btime <= obj1.btime <= obj2.etime or
                obj1.btime <= obj2.btime <= obj1.etime)
