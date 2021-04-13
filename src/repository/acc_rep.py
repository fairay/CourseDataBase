from repository import *
from src.objects.person import *
from src.repository.pw_rep import *


class AccountsRepository(Repository):
    def __init__(self):
        pass


class PWAccountsRep(AccountsRepository):
    def __init__(self):
        pass

    def get(self):
        res = AccountsModel.get()

        obj_arr = []
        for acc in res:
            print(acc.Login)
