import model as bm
import errors as exc
from inject_config import *

from . import *


class CmdDutyView(CmdBaseView):
    @classmethod
    def get_drivers(cls):
        proc = bm.DriverDutyProc('admin')
        duty_arr = proc.get_all()
        duty_arr = cls._tranfrom_dow(proc.dow_long_names, duty_arr)
        return cls._table_str(duty_arr)

    @classmethod
    def get_guards(cls):
        proc = bm.GuardDutyProc('admin')
        duty_arr = proc.get_all()
        duty_arr = cls._tranfrom_dow(proc.dow_long_names, duty_arr)
        return cls._table_str(duty_arr)

    @classmethod
    def _tranfrom_dow(cls, dow_names: [str], d_arr: [dict]):
        for d in d_arr:
            s = '|'
            for day in dow_names:
                if d['dow_view'][day]: s += '+|'
                else:                  s += ' |'
            del d['dow_view']
            d['dow'] = s
        return d_arr
