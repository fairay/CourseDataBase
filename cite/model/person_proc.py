from inject_config import *
from .base_proc import BaseProc
from .acc_proc import AccountProc
from objects import *
import errors as exc


class PersonProc(BaseProc):
    _gender_dict = {'м': 'Мужской', 'ж': 'Женский'}

    def register(self, obj: Person):
        rep_ = inject.instance(PersonRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    def profile_info(self, login: str):
        rep_ = inject.instance(PersonRepository)(self._con)
        person_ = rep_.get_by_login(login)
        return self._profile_info(person_)

    def all_profiles(self, cmp=None, hide_unver=False):
        rep_ = inject.instance(PersonRepository)(self._con)
        profiles = []
        for obj in rep_.get_all():
            prof = self._profile_info(obj)
            if hide_unver:
                prof['type_name'] = prof['type_name'].split('(')[0]

            if cmp is None or cmp(prof['pers_type']):
                profiles.append(prof)

        return profiles

    def _profile_info(self, person_: Person):
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
