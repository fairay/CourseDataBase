from repository.repository import *
from objects.guard_duty import GuardRDuty
from repository.pw_rep import *
from errors import *


class GuardRDutyRepository(Repository):
    def create(self, obj: GuardRDuty): raise NotImplementedError
    def update(self, old_obj: GuardRDuty, new_obj: GuardRDuty): raise NotImplementedError
    def delete(self, obj: GuardRDuty): raise NotImplementedError
    def get_all(self) -> [GuardRDuty]: raise NotImplementedError
    def get_by_time(self, begin_date, end_date=None, login=None, check_id=None) -> [GuardRDuty]: raise NotImplementedError
    def get_by_id(self, id_: int) -> GuardRDuty: raise NotImplementedError


class PWGuardRDutyRep(GuardRDutyRepository):
    _model = None
    _rule_model = None
    _con = None

    def __init__(self, con: Database):
        super().__init__(con)
        self._con = con
        self._model = GuardRDutyModel(con)
        self._rule_model = DutyRulesModel(con)

    def create(self, obj: GuardRDuty):
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
            self._model.insert(checkpointid=d['checkpointid'],
                               login=d['login'],
                               ruleid=d['ruleid']).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: GuardRDuty, new_obj: GuardRDuty):
        return NotImplementedError
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(GuardRDutyModel.dutyid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: GuardRDuty):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._rule_model.delete().where(DutyRulesModel.ruleid == obj.ruleid)
        query.execute()
        query = self._model.delete().where(GuardRDutyModel.dutyid == obj.id)
        query.execute()

    def get_all(self) -> [GuardRDuty]:
        res = self._model.select(GuardRDutyModel, DutyRulesModel)\
            .join(DutyRulesModel, on=(GuardRDutyModel.ruleid == DutyRulesModel.ruleid))
        return request_to_objects(res, GuardRDuty)

    def get_by_time(self, begin_date, end_date=None, login=None, check_id=None) -> [GuardRDuty]:
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
            where_exp &= GuardRDutyModel.login == login
        if check_id is not None:
            where_exp &= GuardRDutyModel.checkpointid == check_id

        res = self._model.select(GuardRDutyModel, DutyRulesModel) \
            .join(DutyRulesModel, on=(GuardRDutyModel.ruleid == DutyRulesModel.ruleid))\
            .switch(self._model).where(where_exp)
        return request_to_objects(res, GuardRDuty)

    def get_by_id(self, check_id: int) -> GuardRDuty:
        res = self._model.select(GuardRDutyModel, DutyRulesModel) \
            .join(DutyRulesModel, on=(GuardRDutyModel.ruleid == DutyRulesModel.ruleid))\
            .switch(self._model)\
            .where(GuardRDutyModel.dutyid == check_id)
        acc_arr = request_to_objects(res, GuardRDuty)
        return acc_arr[0] if len(acc_arr) else None
