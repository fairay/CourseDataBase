import hashlib, uuid
from .base_proc import BaseProc
from inject_config import *
from objects import *
import errors as exc


class AccountProc(BaseProc):
    _type_dict = {'admin': 'Администратор', 'guard': 'Охранник', 'driver': 'Водитель'}

    @staticmethod
    def verified(perstype: str) -> bool: return perstype[0] != '~'
    @staticmethod
    def unverified(perstype: str) -> bool: return perstype[0] == '~'

    @staticmethod
    def get_type_names() -> dict:
        return AccountProc._type_dict

    @staticmethod
    def type_name(perstype: str) -> str:
        if perstype in AccountProc._type_dict.keys():
            return AccountProc._type_dict[perstype]
        if AccountProc.unverified(perstype):
            perstype = perstype[1:]
            if perstype in AccountProc._type_dict.keys():
                return AccountProc._type_dict[perstype] + " (неподтверждённый аккаунт)"
        else:
            return perstype

    @staticmethod
    def _get_cookie(obj: Account) -> dict:
        obj_dict = {
            'login': obj.login,
            'perstype': obj.pers_type,
            'type_name': AccountProc.type_name(obj.pers_type),
        }
        return obj_dict

    def get_cookie(self, login: str):
        rep_ = inject.instance(AccountsRepository)(self._con)
        acc = rep_.get_by_login(login)
        if acc is None:
            raise exc.NoneExistExc()
        return AccountProc._get_cookie(acc)

    def delete(self, login: str):
        rep_ = inject.instance(AccountsRepository)(self._con)
        obj = rep_.get_by_login(login)
        if obj is None:
            raise exc.NoneExistExc('данный логин не зарегистрирован')

        rep_.delete(obj)

    def login(self, login: str, password: str) -> Account or None:
        acc_rep = inject.instance(AccountsRepository)(self._con)
        acc = acc_rep.get_by_login(login)

        if acc is None:
            return None  # TODO: raise not auth
        elif AccountProc._check_password(acc, password):
            return acc
        else:
            return None  # TODO: raise wrong login/password

    # TODO: validation with create
    def create(self, **init_dict):
        if not {'login', 'password', 'perstype'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        rep_ = inject.instance(AccountsRepository)(self._con)
        if rep_.get_by_login(init_dict['login']) is not None:
            raise exc.AlreadyExistsExc()

        if init_dict['perstype'] not in self._type_dict.keys():
            raise exc.WrongFormatExc('некорректная должность')

        init_dict['perstype'] = '~' + init_dict['perstype']
        init_dict['salt'] = self._generate_salt()
        init_dict['hashedpassword'] = self._hash_password(init_dict['password'], init_dict['salt'])
        return Account(**init_dict)

    def register(self, obj: Account):
        rep_ = inject.instance(AccountsRepository)(self._con)
        rep_.create(obj)

    def unregister(self, obj: Account):
        rep_ = inject.instance(AccountsRepository)(self._con)
        rep_.delete(obj)

    def approve(self, login: str):
        rep_ = inject.instance(AccountsRepository)(self._con)

        acc = rep_.get_by_login(login)
        if acc is None:
            raise exc.NonExistentExc()

        if not AccountProc.unverified(acc.pers_type):
            raise exc.VerifiedExc()

        new_acc = acc.clone()
        new_acc.pers_type = acc.pers_type[1:]
        rep_.update(acc, new_acc)

    def get_all(self, role: str = None):
        rep_: AccountsRepository = inject.instance(AccountsRepository)(self._con)

        if role is None: obj_arr = rep_.get_all()
        else:            obj_arr = rep_.get_by_role(role)

        dict_arr = []
        for obj in obj_arr:
            dict_arr.append(obj.to_dict())

        return dict_arr

    def get(self, login: str):
        acc_rep = inject.instance(AccountsRepository)(self._con)
        return acc_rep.get_by_login(login)

    def check_role(self, login: str, role='admin') -> bool:
        acc_rep: AccountsRepository = inject.instance(AccountsRepository)(self._con)
        acc = acc_rep.get_by_login(login)
        if acc is None:
            return False

        if type(role) is str:
            return acc.pers_type == role
        elif type(role) is list:
            for r in role:
                if acc.pers_type == r:
                    return True
        return False

    @staticmethod
    def _generate_salt():
        return uuid.uuid4().hex + uuid.uuid4().hex

    @staticmethod
    def _hash_password(password: str, salt: str):
        salt_pw = password.encode('utf-8') + salt.encode('utf-8')
        return hashlib.sha256(salt_pw).hexdigest()

    @staticmethod
    def _check_password(acc: Account, password: str):
        salt = acc.salt
        hashed_pw = AccountProc._hash_password(password, salt)

        return hashed_pw == acc.get_hashed_password()


class BaseAccCheck(object):
    def check(self, data: dict):
        if 'login' not in data.keys():
            raise exc.NotAuthorisedExc()
        if 'perstype' not in data.keys():
            raise exc.NotAuthorisedExc()


class RoleCheck(BaseAccCheck):
    _allowed_roles = []

    def check(self, data: dict):
        super(RoleCheck, self).check(data)
        if data['perstype'][0] == '~':
            raise exc.UnverifiedExc()
        if data['perstype'] not in self._allowed_roles:
            raise exc.NotAllowedExc()


class AllRoleCheck(RoleCheck): _allowed_roles = ['admin', 'guard', 'driver']
class AdminCheck(RoleCheck):  _allowed_roles = ['admin']
class DriverCheck(RoleCheck): _allowed_roles = ['admin', 'driver']
class OnlyDriverCheck(RoleCheck): _allowed_roles = ['driver']
class GuardCheck(RoleCheck): _allowed_roles = ['admin', 'guard']
class OnlyGuardCheck(RoleCheck): _allowed_roles = ['guard']
