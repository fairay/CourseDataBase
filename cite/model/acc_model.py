import hashlib, uuid
import sys
sys.path.append("..")
from src import *


class AccountModel(object):
    @staticmethod
    def _check_password(acc, password: str):
        salt = acc.get_salt()

        salt_pw = password.encode('utf-8') + salt.encode('utf-8')
        hashed_pw = hashlib.sha256(salt_pw).hexdigest()

        return hashed_pw == acc.get_hashed_password()

    @staticmethod
    def login(login: str, password: str):
        acc_rep = inject.instance(AccountsRepository)
        acc = acc_rep.get_by_login(login)

        if acc is None:
            return None  # TODO: raise not auth
        elif AccountModel._check_password(acc, password):
            return acc
        else:
            return None  # TODO: raise wrong login/password
