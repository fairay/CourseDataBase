import model as bm
import errors as exc
from inject_config import *

from . import *


class CmdUsersView(CmdBaseView):
    @classmethod
    def profile(cls, login: str):
        proc = bm.PersonProc('admin')
        person = proc.profile_info(login)
        return 'Профиль\n' + cls._dict_str(person)

    @classmethod
    def get_all(cls):
        proc = bm.PersonProc('admin')
        person_arr = proc.all_profiles(bm.AccountProc.verified)
        return 'Все пользователи:\n' + cls._table_str(person_arr)

    @classmethod
    def get_unverified(cls):
        proc = bm.PersonProc('admin')
        person_arr = proc.all_profiles(bm.AccountProc.unverified, True)
        return 'Неподтверждённые пользователи:\n' + cls._table_str(person_arr)

    @classmethod
    def approve(cls, login: str):
        msg = 'Ошибка операции подтверждения: '
        proc = bm.AccountProc('admin')
        try:
            proc.approve(login)
        except exc.NonExistentExc:
            return msg + 'аккаунт не зарегистрирован'
        except exc.VerifiedExc:
            return msg + 'аккаунт уже подтверждён'
        except exc.RepositoryExc:
            return msg + 'ошибка на сервере'

        return 'Аккаунт %s успешно подтверждён!\n' % login,\
               cls.get_unverified()
