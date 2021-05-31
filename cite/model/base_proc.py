from inject_config import *
from objects import *
import errors as exc

import re


class BaseProc(object):
    _role: str = None
    _con = None

    def __init__(self, role: str = 'admin', con=None):
        self._con = inject.instance(rep.AdminConnection)

        self._role = role
        if con is not None:
            self._con = con
            return

        cl = None
        if role[0] == '~':
            cl = rep.con_dict['~']
        elif role in rep.con_dict.keys():
            cl = rep.con_dict[role]

        if cl is None:
            raise exc.UnknownRoleExc()

        self._con = inject.instance(cl)

    @staticmethod
    def transform_phone(phone: str) -> str:
        if not re.match(r"\+7[ (-]?[0-9]{3}[ )-]?[0-9]{3}[ -]?[0-9]{2}[ -]?[0-9]{2}", phone):
            return None
        return phone

