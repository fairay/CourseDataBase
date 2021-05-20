from copy import deepcopy


class BaseObj(object):
    def __init__(self, **init_dict):
        pass

    def get_title(self) -> str:
        desc_str = ""
        self_dict = self.to_dict()
        for key in self_dict:
            desc_str += "%25s\t" % key
        return desc_str

    def __str__(self) -> str:
        desc_str = ""
        self_dict = self.to_dict()
        for key in self_dict:
            val = self_dict[key]
            if val is None:
                val = '-'
            desc_str += "%25s\t" % val
        return desc_str

    def __repr__(self):
        return type(self).__name__ + str(self.to_dict())

    def to_dict(self) -> dict:
        return {}

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def clone(self):
        return deepcopy(self)
