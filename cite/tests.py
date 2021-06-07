import unittest as ut
from inject_config import *
import errors as exc
from datetime import *

from repository import *
from objects import *
from repository.pw_rep import *


class BaseRepTest(object):
    _con = SqliteDatabase(':memory:')
    _rep: Repository = None

    _obj_arr: [BaseObj] = []
    _obj_upd: BaseObj = None
    _obj_nonexist: BaseObj = None

    def setUp(self) -> None:
        for obj in self._obj_arr:
            self._rep.create(obj)

    def tearDown(self) -> None:
        self._con.close()

    @staticmethod
    def _sorted_arr(arr: [BaseObj]) -> [BaseObj]:
        raise NotImplementedError

    @staticmethod
    def _equal_len(arr1: [BaseObj], arr2: [BaseObj]) -> bool:
        return len(arr1) == len(arr2)

    @classmethod
    def _equal_content(cls, arr1: [BaseObj], arr2: [BaseObj]) -> bool:
        if not BaseRepTest._equal_len(arr1, arr2):
            return False

        a1 = cls._sorted_arr(arr1)
        a2 = cls._sorted_arr(arr2)

        for i in range(len(a1)):
            if not a1[i] == a2[i]:
                return False
        return True

    def test_select(self):
        rep_arr = self._rep.get_all()

        self.assertTrue(self._equal_len(rep_arr, self._obj_arr))
        self.assertTrue(self._equal_content(rep_arr, self._obj_arr))

    def test_delete(self):
        arr = self._obj_arr.copy()
        del_elem = arr.pop(0)

        self._rep.delete(del_elem)
        rep_arr = self._rep.get_all()

        self.assertTrue(self._equal_len(rep_arr, arr))
        self.assertTrue(self._equal_content(rep_arr, arr))

    def test_repeat(self):
        failed = False
        try:
            self._rep.create(self._obj_arr[0])
        except exc.AlreadyExistsExc:
            failed = True
        self.assertTrue(failed)

        rep_arr = self._rep.get_all()
        self.assertTrue(self._equal_len(rep_arr, self._obj_arr))
        self.assertTrue(self._equal_content(rep_arr, self._obj_arr))

    def test_upd(self):
        arr = self._obj_arr.copy()

        self._rep.update(arr[0], self._obj_upd)
        arr[0] = self._obj_upd

        rep_arr = self._rep.get_all()
        self.assertTrue(self._equal_len(rep_arr, arr))
        self.assertTrue(self._equal_content(rep_arr, arr))

    def test_upd_nonexist(self):
        failed = False
        try:
            self._rep.update(self._obj_nonexist, self._obj_upd)
        except exc.NotExistsExc:
            failed = True
        self.assertTrue(failed)

        rep_arr = self._rep.get_all()
        self.assertTrue(self._equal_len(rep_arr, self._obj_arr))
        self.assertTrue(self._equal_content(rep_arr, self._obj_arr))

    def test_delete_nonexist(self):
        failed = False
        try:
            self._rep.delete(self._obj_nonexist)
        except exc.NotExistsExc:
            failed = True
        self.assertTrue(failed)

        rep_arr = self._rep.get_all()
        self.assertTrue(self._equal_len(rep_arr, self._obj_arr))
        self.assertTrue(self._equal_content(rep_arr, self._obj_arr))


class AccountRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWAccountsRep(_con)

    _obj_upd = Account(login='aboba', perstype='guard', salt='000000', hashedpassword='000000')
    _obj_nonexist = Account(login=' ', perstype=' ', salt=' ', hashedpassword=' ')
    _obj_arr = [
        Account(login='aboba', perstype='admin', salt='1er1r1', hashedpassword='51coms1'),
        Account(login='abiba', perstype='guard', salt='124145', hashedpassword='5121222'),
        Account(login='biba', perstype='driver', salt='ascaasa', hashedpassword='casc'),
        Account(login='boba', perstype='guard', salt='124145', hashedpassword='5121222'),
    ]

    @staticmethod
    def _sorted_arr(arr: [Account]) -> [Account]:
        return sorted(arr, key=lambda x: x.login)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([AccountsModel])
        super(AccountRepTest, self).setUp()

    def test_get_login(self):
        get_obj = self._rep.get_by_login(self._obj_arr[0].login)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_get_login_nonexist(self):
        get_obj = self._rep.get_by_login(self._obj_nonexist.login)
        self.assertEqual(get_obj, None)


class PersonRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWPersonRep(_con)

    _default_data = {"gender": 'м', 'dob': '12.12.1990', 'phonenumber': '+7-916-019-21-22'}
    _obj_upd = Person(login='aboba', forename='Ксения', surname='Иванова', **_default_data)

    _obj_nonexist = Person(login=' ', forename=' ', surname=' ', **_default_data)
    _obj_arr = [
        Person(login='aboba', forename='Ксения', surname='Петрова', **_default_data),
        Person(login='abiba', forename='Валерий', surname='Петров', **_default_data),
        Person(login='biba', forename='Пётр', surname='Иванов', **_default_data),
        Person(login='boba', forename='Павел', surname='Виктор', **_default_data),
    ]

    @staticmethod
    def _sorted_arr(arr: [Person]) -> [Person]:
        return sorted(arr, key=lambda x: x.login)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([PersonModel])
        super(PersonRepTest, self).setUp()

    def test_get_login(self):
        get_obj = self._rep.get_by_login(self._obj_arr[0].login)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_get_login_nonexist(self):
        get_obj = self._rep.get_by_login(self._obj_nonexist.login)
        self.assertEqual(get_obj, None)


class CheckpointsRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWCheckpointsRep(_con)

    _obj_upd = Checkpoint(checkpointid=1, address='ул. Лупин-Пупина', phonenumber='+7 (900) 001-02-03')

    _obj_nonexist = Checkpoint(checkpointid=900, address=' ', phonenumber=' ')
    _obj_arr = [
        Checkpoint(checkpointid=1, address='ул. Пупин-Лупина', phonenumber='+7 (900) 001-02-03'),
        Checkpoint(checkpointid=2, address='ул. Кукушкина, 10к2', phonenumber='8 900 229 69 13'),
        Checkpoint(checkpointid=3, address='ул. Пушкина, 10к2', phonenumber='8 921 292 62 13')
    ]

    @staticmethod
    def _sorted_arr(arr: [Checkpoint]) -> [Checkpoint]:
        return sorted(arr, key=lambda x: x.id)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([CheckpointsModel])
        super(CheckpointsRepTest, self).setUp()

    def test_get_id(self):
        get_obj = self._rep.get_by_id(self._obj_arr[0].id)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_get_id_nonexist(self):
        get_obj = self._rep.get_by_id(self._obj_nonexist.id)
        self.assertEqual(get_obj, None)


class TrucksRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWTrucksRep(_con)

    _obj_upd = Truck(platenumber='П000СО666', category='bmw', model='x6')

    _obj_nonexist = Truck(platenumber=' ', category=' ', model=' ')
    _obj_arr = [
        Truck(platenumber='П000СО666', category='Лада', model='Приора'),
        Truck(platenumber='В000ОР199', category='Жигуль', model='10'),
        Truck(platenumber='С777ОР100', category='Жигуль', model='12'),
    ]

    @staticmethod
    def _sorted_arr(arr: [Truck]) -> [Truck]:
        return sorted(arr, key=lambda x: x.number)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([TrucksModel])
        super(TrucksRepTest, self).setUp()

    def test_get_number(self):
        get_obj = self._rep.get_by_number(self._obj_arr[0].number)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_get_number_nonexist(self):
        get_obj = self._rep.get_by_number(self._obj_nonexist.number)
        self.assertEqual(get_obj, None)


class DeliveryRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWDeliveryRep(_con)

    _obj_upd = Delivery(orderid=1, status='delivered', address='ул. Пушкина', phonenumber='89019123456',
                        creationtime=datetime(2021, 5, 20, 12, 31, 51), login='driver',
                        completiontime=datetime(2021, 5, 21, 8, 30, 2),
                        description='Вези свинину')

    _obj_nonexist = Delivery(orderid=100, status=' ', address=' ', phonenumber=' ',
                             creationtime=datetime(2021, 1, 1),
                             description=' ')
    _obj_arr = [
        Delivery(orderid=1, status='delivered', address='ул. Пушкина', phonenumber='89019123456',
                 creationtime=datetime(2021, 5, 20, 12, 31, 51), login='driver',
                 description='Вези барана'),
        Delivery(orderid=2, status='not_assigned', address='ул. Пушкина', phonenumber='89019123456',
                 creationtime=datetime(2021, 5, 21, 7, 21, 1),
                 description='Хочу шоколад'),
        Delivery(orderid=3, status='in_transit', address='ул. Кукушкина', phonenumber='+79821201921',
                 creationtime=datetime(2021, 5, 20, 23, 5, 15),
                 description='Вези инжир'),
    ]

    @staticmethod
    def _sorted_arr(arr: [Delivery]) -> [Delivery]:
        return sorted(arr, key=lambda x: x.id)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([DeliveryModel])
        super(DeliveryRepTest, self).setUp()

    def test_get_id(self):
        get_obj = self._rep.get_by_id(self._obj_arr[0].id)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_get_id_nonexist(self):
        get_obj = self._rep.get_by_id(self._obj_nonexist.id)
        self.assertEqual(get_obj, None)


class RecordsRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWPassRecordsRep(_con)

    _obj_upd = PassRecord(recordid=1, platenumber='П000СО666', checkpointid=0,
                          passtime=datetime(2021, 5, 20, 12, 31, 51),
                          direction='in')

    _obj_nonexist = PassRecord(recordid=100, platenumber=' ', checkpointid=100,
                               passtime=datetime(2121, 5, 20, 12, 31, 51),
                               direction=' ')
    _obj_arr = [
        PassRecord(recordid=1, platenumber='П000СО666', checkpointid=0,
                   passtime=datetime(2021, 5, 20, 12, 31, 51),
                   direction='out'),
        PassRecord(recordid=2, platenumber='В000ОР199', checkpointid=2,
                   passtime=datetime(2021, 5, 20, 13, 11, 21),
                   direction='in'),
        PassRecord(recordid=3, platenumber='С777ОР100', checkpointid=0,
                   passtime=datetime(2021, 5, 21, 9, 0, 0),
                   direction='in'),
    ]

    @staticmethod
    def _sorted_arr(arr: [PassRecord]) -> [PassRecord]:
        return sorted(arr, key=lambda x: x.id)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([PassRecordsModel])
        super(RecordsRepTest, self).setUp()

    def test_get_id(self):
        get_obj = self._rep.get_by_id(self._obj_arr[0].id)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_get_id_nonexist(self):
        get_obj = self._rep.get_by_id(self._obj_nonexist.id)
        self.assertEqual(get_obj, None)


class GuardRDutyRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWGuardDutyRep(_con)

    _obj_upd = GuardRDuty(dutyid=1, ruleid=1,
                          checkpointid=0, login='guard',
                          begindate=date(2021, 5, 1), enddate=date(2021, 6, 1),
                          begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                          dow='01234')

    _obj_nonexist = GuardRDuty(dutyid=100, ruleid=100, checkpointid=0, login='',
                               begindate=date(2021, 5, 1), enddate=date(2021, 6, 1),
                               begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                               dow='')
    _obj_arr = [
        GuardRDuty(dutyid=1, ruleid=1, checkpointid=0, login='guard',
                  begindate=date(2021, 5, 1),
                  begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                  dow='01234'),
        GuardRDuty(dutyid=2, ruleid=2, checkpointid=2, login='vasyok1997',
                  begindate=date(2021, 5, 1), enddate=date(2021, 6, 1),
                  begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                  dow='01'),
        GuardRDuty(dutyid=3, ruleid=3, checkpointid=1, login='chicksa1999',
                  begindate=date(2021, 1, 1), enddate=date(2022, 1, 1),
                  begintime=time(9, 0, 0), endtime=time(15, 0, 0),
                  dow='0246'),
    ]

    @staticmethod
    def _sorted_arr(arr: [GuardRDuty]) -> [GuardRDuty]:
        return sorted(arr, key=lambda x: x.id)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([DutyRulesModel, GuardDutyModel])
        super(GuardRDutyRepTest, self).setUp()

    def test_get_id(self):
        get_obj = self._rep.get_by_id(self._obj_arr[0].id)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_upd(self): pass
    def test_upd_nonexist(self): pass

    def test_get_id_nonexist(self):
        get_obj = self._rep.get_by_id(self._obj_nonexist.id)
        self.assertEqual(get_obj, None)


class DriverRDutyRepTest(BaseRepTest, ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWDriverDutyRep(_con)

    _obj_upd = DriverRDuty(dutyid=1, ruleid=1,
                           platenumber='П000СО666', login='driver',
                           begindate=date(2021, 5, 1), enddate=date(2021, 6, 1),
                           begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                           dow='01234')

    _obj_nonexist = DriverRDuty(dutyid=100, ruleid=100, platenumber='', login='',
                                begindate=date(2021, 5, 1), enddate=date(2021, 6, 1),
                                begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                                dow='')
    _obj_arr = [
        DriverRDuty(dutyid=1, ruleid=1, platenumber='П000СО666', login='driver',
                    begindate=date(2021, 5, 1),
                    begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                    dow='01234'),
        DriverRDuty(dutyid=2, ruleid=2, platenumber='В000ОР199', login='sanyok1997',
                    begindate=date(2021, 5, 1), enddate=date(2021, 6, 1),
                    begintime=time(9, 0, 0), endtime=time(18, 30, 0),
                    dow='01'),
        DriverRDuty(dutyid=3, ruleid=3, platenumber='С777ОР100', login='chocksa1999',
                    begindate=date(2021, 1, 1), enddate=date(2022, 1, 1),
                    begintime=time(9, 0, 0), endtime=time(15, 0, 0),
                    dow='0246'),
    ]

    @staticmethod
    def _sorted_arr(arr: [DriverRDuty]) -> [DriverRDuty]:
        return sorted(arr, key=lambda x: x.id)

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([DutyRulesModel, DriverDutyModel])
        super(DriverRDutyRepTest, self).setUp()

    def test_get_id(self):
        get_obj = self._rep.get_by_id(self._obj_arr[0].id)
        self.assertEqual(get_obj, self._obj_arr[0])

    def test_upd(self): pass
    def test_upd_nonexist(self): pass

    def test_get_id_nonexist(self):
        get_obj = self._rep.get_by_id(self._obj_nonexist.id)
        self.assertEqual(get_obj, None)


if __name__ == '__main__':
    ut.main()
