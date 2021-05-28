from .base_object import *


class Delivery(BaseObj):
    _id: int = None
    _status: str = None
    _creation_t = None
    _address: str = None
    _phone: str = None
    _descr: str = None

    _login: str = None
    _completion_t = None

    def __init__(self, **init_dict):
        super(Delivery, self).__init__()
        if init_dict is None:
            return

        self._id = init_dict['orderid']
        self._status = init_dict['status']
        self._address = init_dict['address']
        self._phone = init_dict['phonenumber']
        self._creation_t = init_dict['creationtime']
        self._descr = init_dict['description']

        if 'login' in init_dict.keys():
            self._login = init_dict['login']
        if 'completiontime' in init_dict.keys():
            self._completion_t = init_dict['completiontime']

    def to_dict(self) -> dict:
        return {'orderid': self._id,
                'status': self._status,
                'address': self._address,
                'phonenumber': self._phone,
                'creationtime': self._creation_t,
                'description': self._descr,

                'login': self._login,
                'completiontime': self._completion_t,
                }

    def get_id(self): return self._id
    def get_status(self): return self._status
    def get_creation_t(self): return self._creation_t
    def get_address(self): return self._address
    def get_phone(self): return self._phone
    def get_login(self): return self.login
    def get_completion_t(self): return self._completion_t
    def get_descr(self): return self._descr

    def set_id(self, val: int): self._id = val
    def set_status(self, val: str): self._status = val
    def set_creation_t(self, val): self._creation_t = val
    def set_address(self, val: str): self._address = val
    def set_phone(self, val: str): self._phone = val
    def set_login(self, val: str): self._login = val
    def set_completion_t(self, val): self._completion_t = val
    def set_descr(self, val: str): self._descr = val

    id = property(get_id, set_id)
    status = property(get_status, set_status)
    creation_t = property(get_creation_t, set_creation_t)
    address = property(get_address, set_address)
    phone = property(get_phone, set_phone)
    login = property(get_login, set_login)
    completion_t = property(get_completion_t, set_completion_t)
    descr = property(get_descr, set_descr)
