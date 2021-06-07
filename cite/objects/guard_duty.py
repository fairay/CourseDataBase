from .base_duty import BaseDuty


class GuardDuty(BaseDuty):
    _id: int = None
    _checkpoint: int = None
    _login: str = None

    def __init__(self, **init_dict):
        super(GuardDuty, self).__init__(**init_dict)
        if init_dict is None:
            return

        self._id = init_dict['dutyid']
        self._checkpoint = init_dict['checkpointid']
        self._login = init_dict['login']

    def to_dict(self) -> dict:
        d = super(GuardDuty, self).to_dict()
        d['dutyid'] = self._id
        d['checkpointid'] = self._checkpoint
        d['login'] = self._login
        return d

    def get_id(self): return self._id
    def get_checkpoint(self): return self._checkpoint
    def get_login(self): return self._login

    def set_id(self, val: int): self._id = val
    def set_checkpoint(self, val: int): self._checkpoint = val
    def set_login(self, val: str): self._login = val

    id = property(get_id, set_id)
    checkpoint = property(get_checkpoint, set_checkpoint)
    login = property(get_login, set_login)
