from src.objects.base_object import *


class Account(BaseObj):
    _login = None
    _salt = None
    _hashed_password = None
    _pers_type = None

    def __init__(self, **init_dict):
        if init_dict is None:
            return

        self._login = init_dict['login']
        self._pers_type = init_dict['perstype']
        self._salt = init_dict['salt']
        self._hashed_password = init_dict['hashedpassword']

    # def __str__(self):
    #     return 'Login:%30s\tType:%8s\tSalt + Password:%20s %20s' % \
    #            (self._login, self._pers_type, self._salt, self._hashed_password)

    def to_dict(self) -> dict:
        return {'login': self._login, 'perstype': self._pers_type,
                'salt': self._salt, 'hashedpassword': self._hashed_password}

    def get_login(self): return self._login
    def get_salt(self): return self._salt
    def get_hashed_password(self): return self._hashed_password
    def get_pers_type(self): return self._pers_type

    def set_login(self, val): self._login = val
    def set_salt(self, val): self._salt = val
    def set_hashed_password(self, val): self._hashed_password = val
    def set_pers_type(self, val): self._pers_type = val
