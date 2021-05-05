from repository.repository import *
from objects.person import *
from repository.pw_rep import *
from errors import *


class PersonRepository(Repository):
    def create(self, obj: Person): raise NotImplementedError
    def update(self, old_obj: Person, new_obj: Person): raise NotImplementedError
    def delete(self, obj: Person): raise NotImplementedError
    def get_all(self) -> [Person]: raise NotImplementedError


class PWPersonRep(PersonRepository):
    def create(self, obj: Person):
        try:
            PersonModel.create(**obj.to_dict())
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Person, new_obj: Person):
        query = PersonModel. \
            update(**new_obj.to_dict()). \
            where(PersonModel.personid == old_obj.set_id())

        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Person):
        query = PersonModel.delete().where(PersonModel.personid == obj.set_id())
        query.execute()

    def get_all(self) -> [Person]:
        res = PersonModel.select()
        return request_to_objects(res, Person)
