from src.repository.repository import *
from src.objects.account import *
from src.repository.pw_rep import *


class AccountsRepository(Repository):
    def __init__(self):
        pass


class PWAccountsRep(AccountsRepository):
    def __init__(self):
        pass

    def create(self, obj):
        AccountsModel.create(login=obj.get_login(),
                             perstype=obj.get_pers_type(),
                             salt=obj.get_salt(),
                             hashedpassword=obj.get_hashed_password())

    def get(self):
        res = AccountsModel.select()
        return request_to_objects(res, Account)
