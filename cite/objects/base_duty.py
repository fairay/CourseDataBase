from .base_object import *


class BaseDuty(BaseObj):
    _ruleid: int = None
    _bdate = None
    _edate = None
    _btime = None
    _etime = None
    _dow: str = None

    def __init__(self, **init_dict):
        super(BaseDuty, self).__init__(**init_dict)
        if init_dict is None:
            return

        self._ruleid = init_dict['ruleid']
        self._bdate = init_dict['begindate']
        self._btime = init_dict['begintime']
        self._etime = init_dict['endtime']
        self._dow = init_dict['dow']

        if 'enddate' in init_dict.keys():
            self._edate = init_dict['enddate']

    def to_dict(self) -> dict:
        return {'ruleid': self._ruleid,
                'begindate': self._bdate,
                'enddate': self._edate,
                'begintime': self._btime,
                'endtime': self._etime,
                'dow': self._dow,
                }

    def get_ruleid(self): return self._ruleid
    def get_bdate(self): return self._bdate
    def get_edate(self): return self._edate
    def get_btime(self): return self._btime
    def get_etime(self): return self._etime
    def get_dow(self): return self._dow

    def set_ruleid(self, val: int): self._ruleid = val
    def set_bdate(self, val): self._bdate = val
    def set_edate(self, val): self._edate = val
    def set_btime(self, val): self._btime = val
    def set_etime(self, val): self._etime = val
    def set_dow(self, val: str): self._dow = val

    ruleid = property(get_ruleid, set_ruleid)
    bdate = property(get_bdate, set_bdate)
    edate = property(get_edate, set_edate)
    btime = property(get_btime, set_btime)
    etime = property(get_etime, set_etime)
    dow = property(get_dow, set_dow)
