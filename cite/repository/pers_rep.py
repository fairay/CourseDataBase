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
    def create(self, obj: Person):
        try:
            pers_dict = obj.to_dict()
            del pers_dict['personid']
            PersonModel.create(**pers_dict)
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Person, new_obj: Person):
        query = PersonModel. \
            update(**new_obj.to_dict()). \
            where(PersonModel.personid == old_obj.id)

        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Person):
        query = PersonModel.delete().where(PersonModel.personid == obj.id)
        query.execute()

    def get_all(self) -> [Person]:
        res = PersonModel.select()
        return request_to_objects(res, Person)

    def get_by_login(self, login: str) -> Person:
        res = PersonModel.select().where(PersonModel.login == login)
        pers_arr = request_to_objects(res, Person)
        return pers_arr[0] if len(pers_arr) else None
