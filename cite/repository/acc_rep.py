from repository.repository import *
from objects.account import *
from repository.pw_rep import *
from errors import *


class AccountsRepository(Repository):
    def create(self, obj: Account): raise NotImplementedError
    def update(self, old_obj: Account, new_obj: Account): raise NotImplementedError
    def delete(self, obj: Account): raise NotImplementedError
    def get_all(self) -> [Account]: raise NotImplementedError
    def get_by_login(self, login: str) -> Account: raise NotImplementedError


class PWAccountsRep(AccountsRepository):
    _model = None

    # TODO: remove inject.instance(AbstractConnection)
    def __init__(self, con=inject.instance(AbstractConnection)):
        super().__init__(con)
        self._model = AccountsModel(con)

    def create(self, obj: Account):
        try:
            self._model.create(**obj.to_dict())
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Account, new_obj: Account):
        query = self._model.\
            update(**new_obj.to_dict()).\
            where(AccountsModel.login == old_obj.login)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Account):
        query = self._model.delete().where(AccountsModel.login == obj.login)
        query.execute()

    def get_all(self) -> [Account]:
        res = self._model.select()
        return request_to_objects(res, Account)

    def get_by_login(self, login: str) -> Account:
        res = self._model.select().where(AccountsModel.login == login)
        acc_arr = request_to_objects(res, Account)
        return acc_arr[0] if len(acc_arr) else None
