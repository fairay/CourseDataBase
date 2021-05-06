from inject_config import *
from .acc_proc import AccountProc
from objects import *
import errors as exc


class PersonProc(object):
    _gender_dict = {'м': 'Мужской', 'ж': 'Женский'}

    @staticmethod
    def _profile_info(person: Person):
        pers_dict = person.to_dict()
        pers_dict['gender'] = PersonProc._gender_dict[person.get_gender()]
        pers_dict['dob'] = str(pers_dict['dob'])

        acc = AccountProc.get(person.get_login())
        pers_dict['type_name'] = AccountProc.type_name(acc.get_pers_type())

        if pers_dict['phonenumber'] is None:
            pers_dict['phonenumber'] = '-'

        return pers_dict

    @staticmethod
    def profile_info(login: str):
        rep = inject.instance(PersonRepository)
        person = rep.get_by_login(login)
        return PersonProc._profile_info(person)

    @staticmethod
    def all_profiles():
        rep = inject.instance(PersonRepository)
        all_persons = rep.get_all()
        return [PersonProc._profile_info(obj) for obj in all_persons]
