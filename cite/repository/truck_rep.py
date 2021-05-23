from repository.repository import *
from objects.truck import *
from repository.pw_rep import *
from errors import *


class TrucksRepository(Repository):
    def create(self, obj: Truck): raise NotImplementedError
    def update(self, old_obj: Truck, new_obj: Truck): raise NotImplementedError
    def delete(self, obj: Truck): raise NotImplementedError
    def get_all(self) -> [Truck]: raise NotImplementedError
    def get_by_number(self, number: str) -> Truck: raise NotImplementedError


class PWTrucksRep(TrucksRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = TrucksModel(con)

    def create(self, obj: Truck):
        try:
            self._model.insert(**obj.to_dict()).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Truck, new_obj: Truck):
        if self.get_by_number(old_obj.number) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(TrucksModel.platenumber == old_obj.number)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Truck):
        if self.get_by_number(obj.number) is None:
            raise NotExistsExc()

        query = self._model.delete().where(TrucksModel.platenumber == obj.number)
        query.execute()

    def get_all(self) -> [Truck]:
        res = self._model.select()
        return request_to_objects(res, Truck)

    def get_by_number(self, number: str) -> Truck:
        res = self._model.select().where(TrucksModel.platenumber == number)
        acc_arr = request_to_objects(res, Truck)
        return acc_arr[0] if len(acc_arr) else None
