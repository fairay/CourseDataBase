from .base_object import *


class Checkpoint(BaseObj):
    _id: int = None
    _address: str = None
    _phone: str = None

    def __init__(self, **init_dict):
        super(Checkpoint, self).__init__()
        if init_dict is None:
            return

        self._id = init_dict['checkpointid']
        self._address = init_dict['address']
        self._phone = init_dict['phonenumber']

    def to_dict(self) -> dict:
        return {'checkpointid': self._id,
                'address': self._address,
                'phonenumber': self._phone}

    def get_id(self): return self._id
    def get_address(self): return self._address
    def get_phone(self): return self._phone

    def set_id(self, val: int): self._id = val
    def set_address(self, val: str): self._address = val
    def set_phone(self, val: str):  self._phone = val

    id = property(get_id, set_id)
    address = property(get_address, set_address)
    phone = property(get_phone, set_phone)
