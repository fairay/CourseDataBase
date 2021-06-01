import model as bm
import errors as exc
from inject_config import *

from . import *


class CmdAuthView(CmdBaseView):
    @classmethod
    def register(cls, **init_dict) -> str:
        acc_proc = bm.AccountProc('admin')
        pers_proc = bm.PersonProc('admin')

        acc = acc_proc.register(init_dict['login'], init_dict['password'], init_dict['perstype'])
        if acc is None:
            return 'Аккаунт с данным именем уже зарегестрирован, попробуйте другой логин'

        pers = pers_proc.create(**init_dict)
        pers = pers_proc.add(pers)
        if pers is None:
            acc_proc.unregister(acc)
            return 'Ошибка регистрации личных данных'

        return 'Пользователь успешно зарегестрирован.\n' +\
               CmdUsersView.profile(init_dict['login'])
