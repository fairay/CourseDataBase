from .base_object import *


class Truck(BaseObj):
    _number: str = None
    _category: str = None
    _model: str = None

    def __init__(self, **init_dict):
        super(Truck, self).__init__()
        if init_dict is None:
            return

        self._number = init_dict['platenumber']
        self._category = init_dict['category']
        self._model = init_dict['model']

    def to_dict(self) -> dict:
        return {'platenumber': self._number,
                'category': self._category,
                'model': self._model}

    def get_number(self): return self._number
    def get_category(self): return self._category
    def get_model(self): return self._model

    def set_number(self, val: str): self._number = val
    def set_category(self, val: str): self._category = val
    def set_model(self, val: str):  self._model = val

    number = property(get_number, set_number)
    category = property(get_category, set_category)
    model = property(get_model, set_model)
