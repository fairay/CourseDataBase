from repository.repository import *
from objects.guard_duty import *
from repository.pw_rep import *
from errors import *


class GuardDutyRepository(Repository):
    def create(self, obj: GuardDuty): raise NotImplementedError
    def update(self, old_obj: GuardDuty, new_obj: GuardDuty): raise NotImplementedError
    def delete(self, obj: GuardDuty): raise NotImplementedError
    def get_all(self) -> [GuardDuty]: raise NotImplementedError
    def get_by_id(self, id_: int) -> GuardDuty: raise NotImplementedError


class PWGuardDutyRep(GuardDutyRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = GuardDutysModel(con)

    def create(self, obj: GuardDuty):
        try:
            self._model.insert(**obj.to_dict()).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: GuardDuty, new_obj: GuardDuty):
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(GuardDutysModel.dutyid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: GuardDuty):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._model.delete().where(GuardDutysModel.dutyid == obj.id)
        query.execute()

    def get_all(self) -> [GuardDuty]:
        res = self._model.select()
        return request_to_objects(res, GuardDuty)

    def get_by_id(self, check_id: int) -> GuardDuty:
        res = self._model.select().where(GuardDutysModel.dutyid == check_id)
        acc_arr = request_to_objects(res, GuardDuty)
        return acc_arr[0] if len(acc_arr) else None
