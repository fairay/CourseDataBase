from inject_config import *
from .acc_proc import AccountProc
from objects import *
import errors as exc


class PersonProc(object):
    _gender_dict = {'м': 'Мужской', 'ж': 'Женский'}

    @staticmethod
    def register(obj: Person):
        rep_ = inject.instance(PersonRepository)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj

    @staticmethod
    def profile_info(login: str):
        rep = inject.instance(PersonRepository)
        person = rep.get_by_login(login)
        return PersonProc._profile_info(person)

    @staticmethod
    def all_profiles(cmp=None, hide_unver=False):
        rep_ = inject.instance(PersonRepository)
        profiles = []
        for obj in rep_.get_all():
            prof = PersonProc._profile_info(obj)
            if hide_unver:
                prof['type_name'] = prof['type_name'].split('(')[0]

            if cmp is None or cmp(prof['pers_type']):
                profiles.append(prof)

        return profiles

    @staticmethod
    def _profile_info(person: Person):
        pers_dict = person.to_dict()
        pers_dict['gender'] = PersonProc._gender_dict[person.get_gender()]
        pers_dict['dob'] = str(pers_dict['dob'])

        acc = AccountProc.get(person.get_login())
        pers_dict['pers_type'] = acc.get_pers_type()
        pers_dict['type_name'] = AccountProc.type_name(acc.get_pers_type())

        if pers_dict['phonenumber'] is None:
            pers_dict['phonenumber'] = '-'

        return pers_dict
