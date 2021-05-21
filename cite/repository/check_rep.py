from repository.repository import *
from objects.checkpoint import *
from repository.pw_rep import *
from errors import *


class CheckpointsRepository(Repository):
    def create(self, obj: Checkpoint): raise NotImplementedError
    def update(self, old_obj: Checkpoint, new_obj: Checkpoint): raise NotImplementedError
    def delete(self, obj: Checkpoint): raise NotImplementedError
    def get_all(self) -> [Checkpoint]: raise NotImplementedError
    def get_by_id(self, check_id: int) -> Checkpoint: raise NotImplementedError


class PWCheckpointsRep(CheckpointsRepository):
    _model = None
    _con = None

    def __init__(self, con):
        super().__init__(con)
        self._con = con
        self._model = CheckpointsModel(con)

    def create(self, obj: Checkpoint):
        try:
            self._model.insert(**obj.to_dict()).execute()
        except IntegrityError as exc:
            raise AlreadyExistsExc()

    def update(self, old_obj: Checkpoint, new_obj: Checkpoint):
        if self.get_by_id(old_obj.id) is None:
            raise NotExistsExc()

        query = self._model.\
            update(**new_obj.to_dict()).\
            where(CheckpointsModel.checkpointid == old_obj.id)
        try:
            query.execute()
        except IntegrityError as exc:
            raise WrongUpdExc()

    def delete(self, obj: Checkpoint):
        if self.get_by_id(obj.id) is None:
            raise NotExistsExc()

        query = self._model.delete().where(CheckpointsModel.checkpointid == obj.id)
        query.execute()

    def get_all(self) -> [Checkpoint]:
        res = self._model.select()
        return request_to_objects(res, Checkpoint)

    def get_by_id(self, check_id: int) -> Checkpoint:
        res = self._model.select().where(CheckpointsModel.checkpointid == check_id)
        acc_arr = request_to_objects(res, Checkpoint)
        return acc_arr[0] if len(acc_arr) else None
