from .base_object import *


class GuardDuty(BaseObj):
    _id: int = None
    _checkpoint: int = None
    _login: str = None
    _bdate = None
    _edate = None
    _btime = None
    _etime = None
    _dow: str = None

    def __init__(self, **init_dict):
        super(GuardDuty, self).__init__()
        if init_dict is None:
            return

        self._id = init_dict['dutyid']
        self._checkpoint = init_dict['checkpointid']
        self._login = init_dict['login']
        self._bdate = init_dict['begindate']
        self._btime = init_dict['begintime']
        self._etime = init_dict['endtime']
        self._dow = init_dict['dow']

        if 'enddate' in init_dict.keys():
            self._edate = init_dict['enddate']

    def to_dict(self) -> dict:
        return {'dutyid': self._id,
                'checkpointid': self._checkpoint,
                'login': self._login,
                'begindate': self._bdate,
                'enddate': self._edate,
                'begintime': self._btime,
                'endtime': self._etime,
                'dow': self._dow,
                }

    def get_id(self): return self._id
    def get_checkpoint(self): return self._checkpoint
    def get_login(self): return self._login
    def get_bdate(self): return self._bdate
    def get_edate(self): return self._edate
    def get_btime(self): return self._btime
    def get_etime(self): return self._etime
    def get_dow(self): return self._dow

    def set_id(self, val: int): self._id = val
    def set_checkpoint(self, val: int): self._checkpoint = val
    def set_login(self, val: str): self._login = val
    def set_bdate(self, val): self._bdate = val
    def set_edate(self, val): self._edate = val
    def set_btime(self, val): self._btime = val
    def set_etime(self, val): self._etime = val
    def set_dow(self, val: str): self._dow = val

    id = property(get_id, set_id)
    checkpoint = property(get_checkpoint, set_checkpoint)
    login = property(get_login, set_login)
    bdate = property(get_bdate, set_bdate)
    edate = property(get_edate, set_edate)
    btime = property(get_btime, set_btime)
    etime = property(get_etime, set_etime)
    dow = property(get_dow, set_dow)
