from repository.repository import *
from objects.driver_duty import DriverDuty
from repository.pw_rep import *
from errors import *
from datetime import *


class DriverDutyRepository(Repository):
    def create(self, obj: DriverDuty): raise NotImplementedError
    def update(self, old_obj: DriverDuty, new_obj: DriverDuty): raise NotImplementedError
    def delete(self, obj: DriverDuty): raise NotImplementedError
    def get_all(self) -> [DriverDuty]: raise NotImplementedError
    def get_by_time(self, begin_date: date, end_date: date = None, login: str = None, platenumber: str = None) -> [DriverDuty]: raise NotImplementedError
    def get_by_id(self, id_: int) -> DriverDuty: raise NotImplementedError
    def get_current(self, login: str = None, platenumber: str = None, moment: datetime = None) -> [DriverDuty]: raise NotImplementedError


class PWDriverDutyRep(DriverDutyRepository):
    _model = None
    _rule_model = None
    _con = None

    def __init__(self, con: Database):
        super().__init__(con)
        self._con = con
        self._model = DriverDutyModel(con)
        self._rule_model = DutyRulesModel(con)

    def create(self, obj: DriverDuty):
        if obj.id is not None and self.get_by_id(obj.id) is not None:
            raise AlreadyExistsExc()

        try:
            d = obj.to_dict()
            del d['ruleid']
            d['ruleid'] = self._rule_model.insert(begindate=d['begindate'],
                                                  enddate=d['enddate'],
                                                  begintime=d['begintime'],
                                                  endtime=d['endtime'],
                                                  dow=d['dow']).execute()
            del d['dutyid']
            self._model.insert(platenumber=d['platenumber'],
                               login=d['login'],
                               ruleid=d['ruleid']).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: DriverDuty, new_obj: DriverDuty):
        return NotImplementedError
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(DriverDutyModel.dutyid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: DriverDuty):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._rule_model.delete().where(DutyRulesModel.ruleid == obj.ruleid)
        query.execute()
        query = self._model.delete().where(DriverDutyModel.dutyid == obj.id)
        query.execute()

    def get_all(self) -> [DriverDuty]:
        res = self._model.select(DriverDutyModel, DutyRulesModel)\
            .join(DutyRulesModel, on=(DriverDutyModel.ruleid == DutyRulesModel.ruleid))
        return request_to_objects(res, DriverDuty)

    def get_by_time(self, begin_date: date, end_date: date = None,
                    login: str = None, platenumber: str = None) -> [DriverDuty]:
        res = storedf_call(self._con, 'GetDDuty', begin_date, end_date, login, platenumber)
        return dicts_to_objects(res, DriverDuty)

    def get_by_id(self, check_id: int) -> DriverDuty:
        res = self._model.select(DriverDutyModel, DutyRulesModel) \
            .join(DutyRulesModel, on=(DriverDutyModel.ruleid == DutyRulesModel.ruleid))\
            .switch(self._rule_model)\
            .where(DriverDutyModel.dutyid == check_id)
        acc_arr = request_to_objects(res, DriverDuty)
        return acc_arr[0] if len(acc_arr) else None

    def get_current(self, login: str = None, platenumber: str = None,
                    moment: datetime = None) -> [DriverDuty]:
        if moment is None:
            res = storedf_call(self._con, 'CurrentDDuty', login, platenumber)
        else:
            res = storedf_call(self._con, 'MomentDDuty', moment, login, platenumber)
        return dicts_to_objects(res, DriverDuty)
