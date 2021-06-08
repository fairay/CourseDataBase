from repository.repository import *
from objects.guard_duty import GuardDuty
from repository.pw_rep import *
from errors import *
from datetime import *


class GuardDutyRepository(Repository):
    def create(self, obj: GuardDuty): raise NotImplementedError
    def update(self, old_obj: GuardDuty, new_obj: GuardDuty): raise NotImplementedError
    def delete(self, obj: GuardDuty): raise NotImplementedError
    def get_all(self) -> [GuardDuty]: raise NotImplementedError
    def get_by_time(self, begin_date: date, end_date: date = None, login: str = None, check_id: int = None) -> [GuardDuty]: raise NotImplementedError
    def get_by_id(self, id_: int) -> GuardDuty: raise NotImplementedError
    def get_current(self, login: str = None, check_id: int = None) -> [GuardDuty]: raise NotImplementedError


class PWGuardDutyRep(GuardDutyRepository):
    _model = None
    _rule_model = None
    _con = None

    def __init__(self, con: Database):
        super().__init__(con)
        self._con = con
        self._model = GuardDutyModel(con)
        self._rule_model = DutyRulesModel(con)

    def create(self, obj: GuardDuty):
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

    def update(self, old_obj: GuardDuty, new_obj: GuardDuty):
        return NotImplementedError
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(GuardDutyModel.dutyid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: GuardDuty):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._rule_model.delete().where(DutyRulesModel.ruleid == obj.ruleid)
        query.execute()
        query = self._model.delete().where(GuardDutyModel.dutyid == obj.id)
        query.execute()

    def get_all(self) -> [GuardDuty]:
        res = self._model.select(GuardDutyModel, DutyRulesModel)\
            .join(DutyRulesModel, on=(GuardDutyModel.ruleid == DutyRulesModel.ruleid))
        return request_to_objects(res, GuardDuty)

    def get_by_time(self, begin_date: date, end_date: date = None,
                    login: str = None, check_id: int = None) -> [GuardDuty]:
        res = storedf_call(self._con, 'GetGDuty', begin_date, end_date, login, check_id)
        return dicts_to_objects(res, GuardDuty)

    def get_by_id(self, check_id: int) -> GuardDuty:
        res = self._model.select(GuardDutyModel, DutyRulesModel) \
            .join(DutyRulesModel, on=(GuardDutyModel.ruleid == DutyRulesModel.ruleid))\
            .switch(self._model)\
            .where(GuardDutyModel.dutyid == check_id)
        acc_arr = request_to_objects(res, GuardDuty)
        return acc_arr[0] if len(acc_arr) else None

    def get_current(self, login: str = None, check_id: int = None) -> [GuardDuty]:
        res = storedf_call(self._con, 'CurrentGDuty', login, check_id)
        return dicts_to_objects(res, GuardDuty)
