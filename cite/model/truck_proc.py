from inject_config import *
from .base_proc import BaseProc
from objects import *
import errors as exc

import re


class TruckProc(BaseProc):
    @staticmethod
    def create(**init_dict) -> Truck:
        if not {'number', 'region', 'category', 'model'}.issubset(init_dict.keys()):
            raise exc.TruckLackExc()

        if not re.match(r"[АВЕКМНОРСТХ]\d{3}[АВЕКМНОРСТХ]{2}", init_dict['number']):
            raise exc.TruckWrongExc()

        init_dict['platenumber'] = init_dict['number'] + init_dict['region']
        return Truck(**init_dict)

    def get_all(self):
        rep_ = inject.instance(TrucksRepository)(self._con)
        trucks = []
        for obj in rep_.get_all():
            trucks.append(obj.to_dict())

        return trucks

    def add(self, obj: Truck):
        rep_ = inject.instance(TrucksRepository)(self._con)

        try:
            rep_.create(obj)
        except exc.AlreadyExistsExc:
            obj = None

        return obj
