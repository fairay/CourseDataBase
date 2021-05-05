import json
from errors import *


class ConfigLoader(object):
    _file_name = None
    _data = None

    def __init__(self, f_name):
        self._file_name = f_name

        try:
            f = open(self._file_name, 'r')
        except FileNotFoundError as exc:
            raise ConfigMissingExc()
        self._data = json.load(f)
        f.close()

    def save(self):
        if self._file_name is None:
            raise FileNotFoundError

        f = open(self._file_name, 'w')
        json.dump(self._data, f)
        f.close()

    def get_article(self, art_name):
        if art_name in self._data.keys():
            return self._data[art_name]
        else:
            return None
