
class Account(object):
    _login = ""
    _salt = ""
    _hashed_password = ""
    _pers_type = ""

    def __init__(self, dict=None):
        if dict is None:
            return

        self._login = dict['login']
        self._pers_type = dict['perstype']
        self._salt = dict['salt']
        self._hashed_password = dict['hashedpassword']

    def get_login(self): return self._login
    def get_salt(self): return self._salt
    def get_hashed_password(self): return self._hashed_password
    def get_pers_type(self): return self._pers_type
