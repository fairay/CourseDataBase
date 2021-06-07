from .base_duty import BaseDuty


class DriverDuty(BaseDuty):
    _id: int = None
    _number: str = None
    _login: str = None

    def __init__(self, **init_dict):
        super(DriverDuty, self).__init__(**init_dict)
        if init_dict is None:
            return

        self._id = init_dict['dutyid']
        self._number = init_dict['platenumber']
        self._login = init_dict['login']

    def to_dict(self) -> dict:
        d = super(DriverDuty, self).to_dict()
        d['dutyid'] = self._id
        d['platenumber'] = self._number
        d['login'] = self._login
        return d

    def get_id(self): return self._id
    def get_number(self): return self._number
    def get_login(self): return self._login

    def set_id(self, val: int): self._id = val
    def set_number(self, val: str): self._number = val
    def set_login(self, val: str): self._login = val

    id = property(get_id, set_id)
    number = property(get_number, set_number)
    login = property(get_login, set_login)
