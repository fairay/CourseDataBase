import unittest as ut
from inject_config import *
from repository.acc_rep import *
from repository.pers_rep import *
import errors as exc


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


if __name__ == '__main__':
    ut.main()
