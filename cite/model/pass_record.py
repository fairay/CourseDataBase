from inject_config import *
from .base_proc import BaseProc
from objects import *
import errors as exc

from .checkpoint_proc import CheckpointProc
from .truck_proc import TruckProc
from .driver_duty import DriverDutyProc

import re
from datetime import *


class PassRecordProc(BaseProc):
    def create(self, **init_dict) -> PassRecord:
        if not {'checkpointid', 'platenumber'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        if 'direction' in init_dict.keys():
            init_dict['direction'] = 'in'
        else:
            init_dict['direction'] = 'out'

        init_dict['passtime'] = datetime.now()
        init_dict['recordid'] = None
        rec = PassRecord(**init_dict)

        if not CheckpointProc(con=self._con).get(rec.checkpoint):
            raise exc.WrongFormatExc('КПП не существует')
        if TruckProc(con=self._con).get(rec.number) is None:
            raise exc.NoneExistExc('машина не существует')

        return rec

    def get_all(self):
        rep_ = inject.instance(PassRecordsRepository)(self._con)
        pass_arr = []
        for obj in self.sort(rep_.get_all()):
            pass_arr.append(self._to_view(obj))

        return pass_arr

    def get_with_login(self):
        rep_ = inject.instance(PassRecordsRepository)(self._con)
        proc = DriverDutyProc(self._role, self._con)
        pass_arr = []

        for obj in self.sort(rep_.get_all()):
            pass_arr.append(self._to_view(obj))
            duty = proc.get_by_time(obj.time, platenumber=obj.number)
            if len(duty):
                pass_arr[-1]['login'] = duty[0]['login']

        return pass_arr

    def get_by_login(self, login: str):
        rep_ = inject.instance(PassRecordsRepository)(self._con)
        proc = DriverDutyProc(self._role, self._con)
        pass_arr = []

        for obj in self.sort(rep_.get_all()):
            duty = proc.get_by_time(obj.time, platenumber=obj.number)
            if len(duty) and duty[0]['login'] == login:
                pass_arr.append(self._to_view(obj))

        return pass_arr

    def add(self, obj: PassRecord):
        rep_ = inject.instance(PassRecordsRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    @staticmethod
    def sort(arr: [PassRecord]) -> [PassRecord]:
        return sorted(arr, key=lambda obj: obj.time, reverse=True)

    def _to_view(self, obj: PassRecord):
        d = obj.to_dict()
        d['passdate'] = d['passtime'].strftime('%d.%m.%Y')
        d['passtime'] = d['passtime'].strftime('%H:%M:%S')
        return d
