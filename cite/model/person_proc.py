from inject_config import *
from .base_proc import BaseProc
from .acc_proc import AccountProc
from objects import *
import errors as exc

from datetime import *

class PersonProc(BaseProc):
    _gender_dict = {'м': 'Мужчина', 'ж': 'Женщина'}

    def create(self, **init_dict) -> Person:
        if not {'login', 'surname', 'forename', 'dob',
                'gender', 'phonenumber'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        init_dict['dob'] = datetime.strptime(init_dict['dob'], '%Y-%m-%d').date()
        dif = datetime.now().date() - init_dict['dob']
        years = dif.days / 365.25
        if years < 16:
            raise exc.WrongFormatExc('недостаточный возраст для работы')

        if not {init_dict['gender']}.issubset(('м', 'ж')):
            raise exc.WrongFormatExc('некорректный пол')

        init_dict['phonenumber'] = self.transform_phone(init_dict['phonenumber'])
        if init_dict['phonenumber'] is None:
            raise exc.WrongFormatExc('некорректный номер телефона')

        return Person(**init_dict)

    def add(self, obj: Person):
        rep_ = inject.instance(PersonRepository)(self._con)
        rep_.create(obj)

    def delete(self, login: str):
        rep_ = inject.instance(PersonRepository)(self._con)
        obj = rep_.get_by_login(login)
        if obj is None:
            raise exc.NoneExistExc('данный логин не зарегистрирован')
        rep_.delete(obj)

        AccountProc(self._role, self._con).delete(login)

    def profile_info(self, login: str):
        rep_ = inject.instance(PersonRepository)(self._con)
        person_ = rep_.get_by_login(login)
        return self._to_view(person_)

    def all_profiles(self, cmp=None, hide_unver=False):
        rep_ = inject.instance(PersonRepository)(self._con)
        profiles = []
        for obj in rep_.get_all():
            prof = self._to_view(obj)
            if hide_unver:
                prof['type_name'] = prof['type_name'].split('(')[0]

            if cmp is None or cmp(prof['pers_type']):
                profiles.append(prof)

        return profiles

    def _to_view(self, person_: Person) -> dict:
        if person_ is None:
            return None

        pers_dict = person_.to_dict()
        pers_dict['gender'] = PersonProc._gender_dict[person_.gender]
        pers_dict['dob'] = str(pers_dict['dob'])

        proc = AccountProc(con=self._con)
        acc = proc.get(person_.login)
        pers_dict['pers_type'] = acc.get_pers_type()
        pers_dict['type_name'] = AccountProc.type_name(acc.get_pers_type())

        if pers_dict['phonenumber'] is None:
            pers_dict['phonenumber'] = '-'

        return pers_dict
