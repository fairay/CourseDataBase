from repository.repository import *
from objects.person import *
from repository.pw_rep import *
from errors import *


class PersonRepository(Repository):
    def create(self, obj: Person): raise NotImplementedError
    def update(self, old_obj: Person, new_obj: Person): raise NotImplementedError
    def delete(self, obj: Person): raise NotImplementedError
    def get_all(self) -> [Person]: raise NotImplementedError
    def get_by_login(self, login: str) -> Person: raise NotImplementedError


class PWPersonRep(PersonRepository):
    _con = None
    _model = None

    # TODO: remove inject.instance(AbstractConnection)
    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = PersonModel(con)

    def create(self, obj: Person):
        query = self._model.insert(**obj.to_dict())
        try:
            query.execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Person, new_obj: Person):
        if self.get_by_login(old_obj.login) is None:
            raise NotExistsExc()

        query = self._model. \
            update(**new_obj.to_dict()). \
            where(PersonModel.login == old_obj.login)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Person):
        if self.get_by_login(obj.login) is None:
            raise NotExistsExc()

        query = self._model.delete().where(PersonModel.login == obj.login)
        query.execute()

    def get_all(self) -> [Person]:
        res = self._model.select()
        return request_to_objects(res, Person)

    def get_by_login(self, login: str) -> Person:
        res = self._model.select().where(PersonModel.login == login)
        pers_arr = request_to_objects(res, Person)
        return pers_arr[0] if len(pers_arr) else None
