import hashlib, uuid
from inject_config import *
from objects import *
import errors as exc


class AccountProc(object):
    _type_dict = {'admin': 'Администратор', 'guard': 'Охранник'}

    @staticmethod
    def type_name(perstype: str) -> str:
        if perstype in AccountProc._type_dict.keys():
            return AccountProc._type_dict[perstype]
        else:
            return perstype

    @staticmethod
    def get_cookie(obj: Account) -> dict:
        obj_dict = {
            'login': obj.get_login(),
            'perstype': obj.get_pers_type(),
            'type_name': AccountProc.type_name(obj.get_pers_type()),
        }
        return obj_dict

    @staticmethod
    def login(login: str, password: str) -> Account or None:
        acc_rep = inject.instance(AccountsRepository)
        acc = acc_rep.get_by_login(login)

        if acc is None:
            return None  # TODO: raise not auth
        elif AccountProc._check_password(acc, password):
            return acc
        else:
            return None  # TODO: raise wrong login/password

    @staticmethod
    def register(login: str, password: str, perstype: str):
        acc_rep = inject.instance(AccountsRepository)
        old_acc = acc_rep.get_by_login(login)

        if old_acc is not None:
            return  # TODO : raise already exists

        perstype = '~' + perstype
        salt = AccountProc._generate_salt()
        hashedpassword = AccountProc._hash_password(password, salt)

        new_acc = Account(locals())
        acc_rep.create(new_acc)

    @staticmethod
    def get(login: str):
        acc_rep = inject.instance(AccountsRepository)
        return acc_rep.get_by_login(login)

    @staticmethod
    def _generate_salt():
        return uuid.uuid4().hex + uuid.uuid4().hex

    @staticmethod
    def _hash_password(password: str, salt: str):
        salt_pw = password.encode('utf-8') + salt.encode('utf-8')
        return hashlib.sha256(salt_pw).hexdigest()

    @staticmethod
    def _check_password(acc, password: str):
        salt = acc.get_salt()
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
class GuardCheck(RoleCheck): _allowed_roles = ['admin', 'guard']
