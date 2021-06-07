from inject_config import *
from .base_proc import BaseProc
from objects import *
import errors as exc

import re


class CheckpointProc(BaseProc):
    @staticmethod
    def create(**init_dict) -> Checkpoint:
        if not {'address', 'phonenumber'}.issubset(init_dict.keys()):
            raise exc.CheckpointLackExc()

        init_dict['phonenumber'] = CheckpointProc.transform_phone(init_dict['phonenumber'])
        if init_dict['phonenumber'] is None:
            raise exc.CheckpointWrongExc()
        init_dict['checkpointid'] = None

        return Checkpoint(**init_dict)

    def get(self, id_: int):
        rep_ = inject.instance(CheckpointsRepository)(self._con)
        return rep_.get_by_id(id_)

    def get_all(self):
        rep_ = inject.instance(CheckpointsRepository)(self._con)
        checkpoints = []
        for obj in rep_.get_all():
            checkpoints.append(obj.to_dict())

        return checkpoints

    def add(self, obj: Checkpoint):
        rep_ = inject.instance(CheckpointsRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj
