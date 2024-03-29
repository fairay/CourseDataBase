from inject_config import *
from .base_proc import BaseProc
from .acc_proc import AccountProc
from .checkpoint_proc import CheckpointProc
from .base_duty import BaseDutyProc
from objects import *
import errors as exc

import re
from datetime import *


class GuardDutyProc(BaseDutyProc):
    def create(self, **init_dict) -> GuardDuty:
        if not {'checkpointid', 'login', 'begindate', 'enddate', 'begintime',
                'endtime', 'dow'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        init_dict = self._pre_create(**init_dict)

        if not AccountProc(con=self._con).check_role(init_dict['login'], 'guard'):
            raise exc.WrongFormatExc('аккаунт не пренадлежит охраннику')
        if CheckpointProc(con=self._con).get(init_dict['checkpointid']) is None:
            raise exc.NoneExistExc('КПП не существует')

        duty = GuardDuty(**init_dict)

        if not self.is_guard_free(duty):
            raise exc.WrongFormatExc('охранник занят в данный период')
        if not self.is_checkpoint_free(duty):
            raise exc.WrongFormatExc('КПП занят в данный период')
        return duty

    def is_guard_free(self, obj: GuardDuty) -> bool:
        rep_: GuardDutyRepository = inject.instance(GuardDutyRepository)(self._con)
        for other in rep_.get_by_time(obj.bdate, obj.edate, login=obj.login):
            if self._is_collide(obj, other):
                return False
        return True

    def is_checkpoint_free(self, obj: GuardDuty) -> bool:
        rep_: GuardDutyRepository = inject.instance(GuardDutyRepository)(self._con)
        for other in rep_.get_by_time(obj.bdate, obj.edate, check_id=obj.checkpoint):
            if self._is_collide(obj, other):
                return False
        return True

    def get_current_view(self, login: str = None):
        duty_arr = []
        for obj in self.get_current(login):
            duty_arr.append(self._to_view(obj))
        return duty_arr

    def get_current(self, login: str = None):
        rep_: GuardDutyRepository = inject.instance(GuardDutyRepository)(self._con)
        duty_arr = rep_.get_current(login)
        return duty_arr

    def get_all(self, login: str = None):
        rep_ = inject.instance(GuardDutyRepository)(self._con)
        duty_arr = []
        for obj in rep_.get_all():
            if login is None or obj.login == login:
                duty_arr.append(self._to_view(obj))

        return duty_arr

    def get_closest(self, login: str):
        rep_: GuardDutyRepository = inject.instance(GuardDutyRepository)(self._con)

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

    def add(self, obj: GuardDuty):
        rep_ = inject.instance(GuardDutyRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj
