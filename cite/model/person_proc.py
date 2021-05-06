from inject_config import *
from objects import *
import errors as exc


class PersonProc(object):
    _gender_dict = {'м': 'Мужской', 'ж': 'Женский'}

    @staticmethod
    def profile_info(login: str):
        rep = inject.instance(PersonRepository)
        person = rep.get_by_login(login)

        pers_dict = person.to_dict()
        pers_dict['gender'] = PersonProc._gender_dict[person.get_gender()]
        return pers_dict
