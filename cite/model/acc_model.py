import hashlib, uuid
from inject_config import *
from objects import *


class AccountProc(object):
    @staticmethod
    def login(login: str, password: str):
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
