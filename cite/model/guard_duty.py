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

        init_dict['dutyid'] = None
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

    def get_current(self):
        rep_: GuardDutyRepository = inject.instance(GuardDutyRepository)(self._con)
        duty_arr = []
        now_date = datetime.now().date()
        for obj in rep_.get_by_time(now_date, now_date):
            if self._is_active(obj):
                duty_arr.append(self._to_view(obj))

        return duty_arr

    def get_all(self):
        rep_ = inject.instance(GuardDutyRepository)(self._con)
        duty_arr = []
        for obj in rep_.get_all():
            duty_arr.append(self._to_view(obj))

        return duty_arr

    def add(self, obj: GuardDuty):
        rep_ = inject.instance(GuardDutyRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    def _to_view(self, obj: GuardDuty):
        d = obj.to_dict()
        d['begindate'] = d['begindate'].strftime('%d.%m.%Y')
        if d['enddate'] is not None:
            d['enddate'] = d['enddate'].strftime('%d.%m.%Y')

        d['dow_view'] = self._dow_view(d['dow'])
        d['begintime'] = d['begintime'].strftime('%H:%M')
        d['endtime'] = d['endtime'].strftime('%H:%M')
        return d

    @staticmethod
    def _is_collide(obj1: GuardDuty, obj2: GuardDuty):
        dow_inter = set(obj2.dow).intersection(obj1.dow)
        if not len(dow_inter):
            return False

        return (obj2.btime <= obj1.btime <= obj2.etime or
                obj1.btime <= obj2.btime <= obj1.etime)
