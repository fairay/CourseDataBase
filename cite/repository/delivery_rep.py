from repository.repository import *
from objects.delivery import *
from repository.pw_rep import *
from errors import *


class DeliveryRepository(Repository):
    def create(self, obj: Delivery): raise NotImplementedError
    def update(self, old_obj: Delivery, new_obj: Delivery): raise NotImplementedError
    def delete(self, obj: Delivery): raise NotImplementedError
    def get_all(self) -> [Delivery]: raise NotImplementedError
    def get_by_login(self, login: str) -> [Delivery]: raise NotImplementedError
    def get_by_id(self, del_id: int) -> Delivery: raise NotImplementedError


class PWDeliveryRep(DeliveryRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = DeliveryModel(con)

    def create(self, obj: Delivery):
        if obj.id is not None and self.get_by_id(obj.id) is not None:
            raise AlreadyExistsExc()

        try:
            d = obj.to_dict()
            del d['orderid']
            self._model.insert(**d).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Delivery, new_obj: Delivery):
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(DeliveryModel.orderid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Delivery):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._model.delete().where(DeliveryModel.orderid == obj.id)
        query.execute()

    def get_all(self) -> [Delivery]:
        res = self._model.select()
        return request_to_objects(res, Delivery)

    def get_by_id(self, check_id: int) -> Delivery:
        res = self._model.select().where(DeliveryModel.orderid == check_id)
        acc_arr = request_to_objects(res, Delivery)
        return acc_arr[0] if len(acc_arr) else None

    def get_by_login(self, login: str) -> [Delivery]:
        res = self._model.select().where(DeliveryModel.login == login)
        return request_to_objects(res, Delivery)
