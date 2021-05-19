from inject_config import *
from objects import *
import errors as exc


class BaseProc(object):
    _role = None
    _con = None

    def __init__(self, role: str = 'admin'):
        self._role = role
        cl = None
        if role[0]:
            cl = rep.con_dict['~']
        elif role in rep.con_dict.keys():
            cl = rep.con_dict[role]

        if cl is None:
            raise exc.UnknownRoleExc()

        self._con = inject.instance(cl)