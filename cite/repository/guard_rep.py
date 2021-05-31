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
    def get_by_time(self, begin_date, end_date=None, login=None, check_id=None) -> [GuardDuty]: raise NotImplementedError


class PWGuardDutyRep(GuardDutyRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = GuardDutysModel(con)

    def create(self, obj: GuardDuty):
        if obj.id is not None and self.get_by_id(obj.id) is not None:
            raise AlreadyExistsExc()

        try:
            d = obj.to_dict()
            del d['dutyid']
            self._model.insert(**d).execute()
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

    def get_by_time(self, begin_date, end_date=None, login=None, check_id=None) -> [GuardDuty]:
        if end_date is None:
            where_exp = GuardDutysModel.enddate.is_null() | (GuardDutysModel.enddate >= begin_date)
        else:
            where_exp = GuardDutysModel.enddate.is_null() & (GuardDutysModel.begindate <= end_date)
            where_exp |= ~GuardDutysModel.enddate.is_null() & (
                    GuardDutysModel.begindate.between(begin_date, end_date) |
                    GuardDutysModel.enddate.between(begin_date, end_date)
            )

        if login is not None:
            where_exp &= GuardDutysModel.login == login
        if check_id is not None:
            where_exp &= GuardDutysModel.checkpointid == check_id

        res = self._model.select().where(where_exp)
        return request_to_objects(res, GuardDuty)
