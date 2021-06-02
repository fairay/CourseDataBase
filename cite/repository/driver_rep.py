from repository.repository import *
from objects.driver_duty import *
from repository.pw_rep import *
from errors import *


class DriverDutyRepository(Repository):
    def create(self, obj: DriverDuty): raise NotImplementedError
    def update(self, old_obj: DriverDuty, new_obj: DriverDuty): raise NotImplementedError
    def delete(self, obj: DriverDuty): raise NotImplementedError
    def get_all(self) -> [DriverDuty]: raise NotImplementedError
    def get_by_time(self, begin_date, end_date=None, login=None, platenumber=None) -> [DriverDuty]: raise NotImplementedError
    def get_by_id(self, id_: int) -> DriverDuty: raise NotImplementedError


class PWDriverDutyRep(DriverDutyRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = DriverDutysModel(con)

    def create(self, obj: DriverDuty):
        if obj.id is not None and self.get_by_id(obj.id) is not None:
            raise AlreadyExistsExc()

        try:
            d = obj.to_dict()
            del d['dutyid']
            self._model.insert(**d).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: DriverDuty, new_obj: DriverDuty):
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(DriverDutysModel.dutyid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: DriverDuty):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._model.delete().where(DriverDutysModel.dutyid == obj.id)
        query.execute()

    def get_all(self) -> [DriverDuty]:
        res = self._model.select()
        return request_to_objects(res, DriverDuty)

    def get_by_time(self, begin_date, end_date=None, login=None, platenumber=None) -> [DriverDuty]:
        if end_date is None:
            where_exp = DriverDutysModel.enddate.is_null() | (DriverDutysModel.enddate >= begin_date)
        else:
            where_exp = DriverDutysModel.enddate.is_null() & (DriverDutysModel.begindate <= end_date)
            where_exp |= ~DriverDutysModel.enddate.is_null() & (
                    DriverDutysModel.begindate.between(begin_date, end_date) |
                    DriverDutysModel.enddate.between(begin_date, end_date) |
                    ((DriverDutysModel.begindate <= end_date) & (end_date <= DriverDutysModel.enddate))
            )

        if login is not None:
            where_exp &= DriverDutysModel.login == login
        if platenumber is not None:
            where_exp &= DriverDutysModel.platenumber == platenumber

        res = self._model.select().where(where_exp)
        return request_to_objects(res, DriverDuty)

    def get_by_id(self, check_id: int) -> DriverDuty:
        res = self._model.select().where(DriverDutysModel.dutyid == check_id)
        acc_arr = request_to_objects(res, DriverDuty)
        return acc_arr[0] if len(acc_arr) else None
