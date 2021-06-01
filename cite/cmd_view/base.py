import model as bm
import errors as exc
from inject_config import *

from . import *
from prettytable import PrettyTable


class CmdBaseView(object):
    @classmethod
    def _obj_str(cls, obj: bm.BaseObj):
        s = ''
        for key, val in obj.to_dict().items():
            s += '%-20s|\t%s\n' % (key, val)
        return s

    @classmethod
    def _dict_str(cls, d: dict):
        s = ''
        for key, val in d.items():
            s += '%-20s|\t%s\n' % (key, val)
        return s

    @classmethod
    def _table_str(cls, d_arr: [dict]):
        th = list(d_arr[0].keys())
        td = []

        for d in d_arr:
            for key, val in d.items():
                td.append(val)

        columns = len(th)
        table = PrettyTable(th)
        td_data = td[:]
        while td_data:
            table.add_row(td_data[:columns])
            td_data = td_data[columns:]

        return str(table)

