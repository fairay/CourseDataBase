from repository.repository import *
from objects.driver_duty import DriverRDuty
from repository.pw_rep import *
from errors import *


class DriverRDutyRepository(Repository):
    def create(self, obj: DriverRDuty): raise NotImplementedError
    def update(self, old_obj: DriverRDuty, new_obj: DriverRDuty): raise NotImplementedError
    def delete(self, obj: DriverRDuty): raise NotImplementedError
    def get_all(self) -> [DriverRDuty]: raise NotImplementedError
    def get_by_time(self, begin_date, end_date=None, login=None, platenumber=None) -> [DriverRDuty]: raise NotImplementedError
    def get_by_id(self, id_: int) -> DriverRDuty: raise NotImplementedError


class PWDriverRDutyRep(DriverRDutyRepository):
    _model = None
    _rule_model = None
    _con = None

    def __init__(self, con: Database):
        super().__init__(con)
        self._con = con
        self._model = DriverRDutyModel(con)
        self._rule_model = DutyRulesModel(con)

    def create(self, obj: DriverRDuty):
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
            print("!!!", exc)
            raise AlreadyExistsExc()

    def update(self, old_obj: DriverRDuty, new_obj: DriverRDuty):
        return NotImplementedError
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(DriverRDutyModel.dutyid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: DriverRDuty):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._rule_model.delete().where(DutyRulesModel.ruleid == obj.ruleid)
        query.execute()
        query = self._model.delete().where(DriverRDutyModel.dutyid == obj.id)
        query.execute()

    def get_all(self) -> [DriverRDuty]:
        res = self._model.select(DriverRDutyModel, DutyRulesModel)\
            .join(DutyRulesModel, on=(DriverRDutyModel.ruleid == DutyRulesModel.ruleid))
        return request_to_objects(res, DriverRDuty)

    def get_by_time(self, begin_date, end_date=None, login=None, platenumber=None) -> [DriverRDuty]:
        if end_date is None:
            where_exp = DutyRulesModel.enddate.is_null() | (DutyRulesModel.enddate >= begin_date)
        else:
            where_exp = DutyRulesModel.enddate.is_null() & (DutyRulesModel.begindate <= end_date)
            where_exp |= ~DutyRulesModel.enddate.is_null() & (
                    DutyRulesModel.begindate.between(begin_date, end_date) |
                    DutyRulesModel.enddate.between(begin_date, end_date) |
                    ((DutyRulesModel.begindate <= end_date) & (end_date <= DutyRulesModel.enddate))
            )

        # TODO: refactor to stored function call
        # print(storedf_call(self._con, 'ddutyinf', begin_date))

        if login is not None:
            where_exp &= DriverRDutyModel.login == login
        if platenumber is not None:
            where_exp &= DriverRDutyModel.platenumber == platenumber

        res = self._model.select(DriverRDutyModel, DutyRulesModel) \
            .join(DutyRulesModel, on=(DriverRDutyModel.ruleid == DutyRulesModel.ruleid))\
            .switch(self._model).where(where_exp)
        return request_to_objects(res, DriverRDuty)

    def get_by_id(self, check_id: int) -> DriverRDuty:
        res = self._model.select(DriverRDutyModel, DutyRulesModel) \
            .join(DutyRulesModel, on=(DriverRDutyModel.ruleid == DutyRulesModel.ruleid))\
            .switch(self._model)\
            .where(DriverRDutyModel.dutyid == check_id)
        acc_arr = request_to_objects(res, DriverRDuty)
        return acc_arr[0] if len(acc_arr) else None
