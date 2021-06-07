from repository.repository import *
from objects.pass_record import *
from objects.guard_duty import GuardRDuty
from repository.pw_rep import *
from errors import *

from datetime import *


class PassRecordsRepository(Repository):
    def create(self, obj: PassRecord): raise NotImplementedError
    def update(self, old_obj: PassRecord, new_obj: PassRecord): raise NotImplementedError
    def delete(self, obj: PassRecord): raise NotImplementedError
    def get_all(self) -> [PassRecord]: raise NotImplementedError
    def get_by_id(self, id_: int) -> PassRecord: raise NotImplementedError
    def get_by_duty(self, duty: GuardRDuty, d: date) -> [PassRecord]: raise NotImplementedError


class PWPassRecordsRep(PassRecordsRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = PassRecordsModel(con)

    def create(self, obj: PassRecord):
        if obj.id is not None and self.get_by_id(obj.id) is not None:
            raise AlreadyExistsExc()

        try:
            d = obj.to_dict()
            del d['recordid']
            self._model.insert(**d).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: PassRecord, new_obj: PassRecord):
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(PassRecordsModel.recordid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: PassRecord):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._model.delete().where(PassRecordsModel.recordid == obj.id)
        query.execute()

    def get_all(self) -> [PassRecord]:
        res = self._model.select()
        return request_to_objects(res, PassRecord)

    def get_by_id(self, id_: int) -> PassRecord:
        res = self._model.select().where(PassRecordsModel.recordid == id_)
        acc_arr = request_to_objects(res, PassRecord)
        return acc_arr[0] if len(acc_arr) else None

    def get_by_checkpoint(self, check_id: int) -> [PassRecord]:
        res = self._model.select().where(PassRecordsModel.checkpointid == check_id)
        return request_to_objects(res, PassRecord)

    def get_by_duty(self, duty: GuardRDuty, d: date) -> [PassRecord]:
        btime = datetime.combine(d, duty.btime)
        etime = datetime.combine(d, duty.etime)
        res = self._model.select().where(
            (PassRecordsModel.checkpointid == duty.checkpoint) &
            PassRecordsModel.passtime.between(btime, etime)
        )
        return request_to_objects(res, PassRecord)
