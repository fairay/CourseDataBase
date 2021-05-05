from src.repository.repository import *
from src.objects.account import *
from src.repository.pw_rep import *
from src.errors import *


class AccountsRepository(Repository):
    def create(self, obj: Account): raise NotImplementedError
    def update(self, old_obj: Account, new_obj: Account): raise NotImplementedError
    def delete(self, obj: Account): raise NotImplementedError
    def get_all(self) -> [Account]: raise NotImplementedError
    def get_by_login(self, login: str) -> Account: raise NotImplementedError


class PWAccountsRep(AccountsRepository):
    def create(self, obj: Account):
        try:
            AccountsModel.create(**obj.to_dict())
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Account, new_obj: Account):
        query = AccountsModel.\
            update(**new_obj.to_dict()).\
            where(AccountsModel.login == old_obj.get_login())
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Account):
        query = AccountsModel.delete().where(AccountsModel.login == obj.get_login())
        query.execute()

    def get_all(self) -> [Account]:
        res = AccountsModel.select()
        return request_to_objects(res, Account)

    def get_by_login(self, login: str) -> Account:
        res = AccountsModel.select().where(AccountsModel.login == login)
        return request_to_objects(res, Account)[0]
