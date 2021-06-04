from .base_object import *
import datetime as dt


class Person(BaseObj):
    # _id = None
    _login = None
    _surname = None
    _forename = None
    _dob = None
    _gender = None
    _phone = None

    def __init__(self, **init_dict):
        super(Person, self).__init__()
        if init_dict is None:
            return

        self._login = init_dict['login']
        self._surname = init_dict['surname']
        self._forename = init_dict['forename']
        self._phone = init_dict['phonenumber']
        self._dob = init_dict['dob']
        self._gender = init_dict['gender']

        # if "personid" in init_dict:
        #     self._id = init_dict['personid']

    def to_dict(self) -> dict:
        return {'login': self._login, 'surname': self._surname,
                'forename': self._forename, 'dob': self._dob, 'gender': self._gender,
                'phonenumber': self._phone}

    # def get_id(self): return self._id
    def get_login(self): return self._login
    def get_surname(self): return self._surname
    def get_forename(self): return self._forename
    def get_dob(self): return self._dob
    def get_gender(self): return self._gender
    def get_phone(self): return self._phone

    # def set_id(self, val): self._id = val
    def set_login(self, val): self._login = val
    def set_surname(self, val): self._surname = val
    def set_forename(self, val): self._forename = val
    def set_dob(self, val):  self._dob = val
    def set_gender(self, val):  self._gender = val
    def set_phone(self, val):  self._phone = val

    # id = property(get_id, set_id)
    login = property(get_login, set_login)
    surname = property(get_surname, set_surname)
    forename = property(get_forename, set_forename)
    dob = property(get_dob, set_dob)
    gender = property(get_gender, set_gender)
    phone = property(get_phone, set_phone)
