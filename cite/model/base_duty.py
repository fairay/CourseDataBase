from inject_config import *
from .base_proc import BaseProc
from .acc_proc import AccountProc
from .truck_proc import TruckProc
from objects import *
import errors as exc

import re
from datetime import *


class BaseDutyProc(BaseProc):
    dow_short_names = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    dow_long_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

    def _pre_create(self, **init_dict) -> dict:
        if not {'login', 'begindate', 'enddate', 'begintime',
                'endtime', 'dow'}.issubset(init_dict.keys()):
            raise exc.LackArgExc()

        init_dict['begintime'] = datetime.strptime(init_dict['begintime'], '%H:%M').time()
        init_dict['endtime'] = datetime.strptime(init_dict['endtime'], '%H:%M').time()
        if init_dict['begintime'] >= init_dict['endtime']:
            raise exc.WrongFormatExc('время начала смены больше времени завершения')

        if not init_dict['dow']:
            raise exc.WrongFormatExc()
        init_dict['dow'] = self._dow_db(init_dict['dow'])

        init_dict['begindate'] = datetime.strptime(init_dict['begindate'], '%Y-%m-%d')
        init_dict['enddate'] = datetime.strptime(init_dict['enddate'], '%Y-%m-%d')

        if 'no_end' in init_dict.keys():
            init_dict['enddate'] = None
        elif init_dict['begindate'] > init_dict['enddate']:
            raise exc.WrongFormatExc('дата начала смены больше даты окончания')

        return init_dict

    def _dow_view(self, dow_str: str, short=False) -> dict:
        if short:
            title_arr = self.dow_short_names
        else:
            title_arr = self.dow_long_names

        dow_dict = {}
        for val in title_arr:
            dow_dict[val] = False

        for day in dow_str:
            dow_dict[title_arr[int(day)]] = True

        return dow_dict

    def _dow_db(self, dow_lst: [str]) -> str:
        ans_str = ''
        for i in range(len(self.dow_short_names)):
            if self.dow_short_names[i] in dow_lst:
                ans_str = ans_str + str(i)

        return ans_str

    @staticmethod
    def _is_active(obj, now):
        # now = datetime.now()
        if not str(now.weekday()) in obj.dow:
            return False

        return obj.btime <= now.time() <= obj.etime
