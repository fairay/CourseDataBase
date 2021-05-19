import unittest as ut
from inject_config import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from repository.acc_rep import *


class AccountRepTest(ut.TestCase):
    _con = SqliteDatabase(':memory:')
    _rep = PWAccountsRep(_con)
    source_arr = [
        Account(login='aboba', perstype='admin', salt='1er1r1', hashedpassword='51coms1'),
        Account(login='abiba', perstype='guard', salt='124145', hashedpassword='5121222'),
    ]

    def setUp(self) -> None:
        self._con.connect()
        self._con.create_tables([AccountsModel])

        print(self._rep.get_all())
        for acc in self.source_arr:
            print('OK')
            self._rep.create(acc)

    def test_select(self) -> None:
        rep_arr = self._rep.get_all()
        a1 = sorted(rep_arr, key=lambda x: x.login)
        a2 = sorted(self.source_arr, key=lambda x: x.login)

        print(a1)
        print(a2)
        self.assertEqual(len(a1), len(a2))
        for i in range(len(a1)):
            self.assertEqual(a1[i], a2[i])


if __name__ == '__main__':
    ut.main()
