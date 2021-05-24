from .base_object import *


class PassRecord(BaseObj):
    _id: int = None
    _number: str = None
    _checkpoint: int = None
    _time = None
    _dir: str = None

    def __init__(self, **init_dict):
        super(PassRecord, self).__init__()
        if init_dict is None:
            return

        self._id = init_dict['recordid']
        self._number = init_dict['platenumber']
        self._checkpoint = init_dict['checkpointid']
        self._time = init_dict['passtime']
        self._dir = init_dict['direction']

    def to_dict(self) -> dict:
        return {'recordid': self._id,
                'platenumber': self._number,
                'checkpointid': self._checkpoint,
                'passtime': self._time,
                'direction': self._dir,
                }

    def get_id(self): return self._id
    def get_number(self): return self._number
    def get_checkpoint(self): return self._checkpoint
    def get_time(self): return self._time
    def get_dir(self): return self._dir

    def set_id(self, val: int): self._id = val
    def set_number(self, val: str): self._number = val
    def set_checkpoint(self, val: int): self._checkpoint = val
    def set_time(self, val): self._time = val
    def set_dir(self, val: str): self._dir = val

    id = property(get_id, set_id)
    number = property(get_number, set_number)
    checkpoint = property(get_checkpoint, set_checkpoint)
    time = property(get_time, set_time)
    dir = property(get_dir, set_dir)

