import model as bm
import errors as exc
from inject_config import *

from . import *


class CmdEntityView(CmdBaseView):
    @classmethod
    def get_trucks(cls):
        proc = bm.TruckProc('admin')
        truck_arr = proc.get_all()
        return 'Машины:\n' + cls._table_str(truck_arr)

    @classmethod
    def get_checkpoints(cls):
        proc = bm.CheckpointProc('admin')
        check_arr = proc.get_all()
        return 'КПП:\n' + cls._table_str(check_arr)

    @classmethod
    def get_delivery(cls):
        proc = bm.DeliveryProc('admin')
        del_arr = proc.get_all()
        return 'Заказы:\n' + cls._table_str(del_arr)

    @classmethod
    def get_pass_records(cls):
        proc = bm.PassRecordProc('admin')
        pass_arr = proc.get_all()
        return 'Записи проезда:\n' + cls._table_str(pass_arr)

    @classmethod
    def delivery_page(cls, orderid: int):
        proc = bm.DeliveryProc('admin')
        order = proc.delivery_info(orderid)
        return 'Страница заказа:\n' + cls._dict_str(order)
