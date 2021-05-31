import inject
import peewee
from playhouse.postgres_ext import *
import config_loader
import repository.repository as rep
from repository.pw_db import DBFromConfig

from repository import *
# TODO: delete
# from repository.pers_rep import PersonRepository, PWPersonRep
# from repository.acc_rep import AccountsRepository, PWAccountsRep
# from repository.truck_rep import TrucksRepository, PWTrucksRep
# from repository.check_rep import CheckpointsRepository, PWCheckpointsRep
# from repository.delivery_rep import DeliveryRepository, PWDeliveryRep
# from repository.driver_rep import DriverDutyRepository, PWDriverDutyRep
# from repository.guard_rep import GuardDutyRepository, PWGuardDutyRep
# from repository.record_rep import PassRecordsRepository, PWPassRecordsRep


def inject_config_db(binder):
    binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('config.json'))

    binder.bind_to_constructor(rep.AbstractConnection,
        lambda: DBFromConfig(inject.instance(peewee.Database),
                             inject.instance(config_loader.ConfigLoader).get_article('admin_connect')))
    binder.bind_to_constructor(rep.TestConnection,
        lambda: peewee.SqliteDatabase(':memory:'))
    binder.bind_to_constructor(rep.AdminConnection,
        lambda: DBFromConfig(inject.instance(peewee.Database),
                             inject.instance(config_loader.ConfigLoader).get_article('admin_connect')))
    binder.bind_to_constructor(rep.GuardConnection,
        lambda: DBFromConfig(inject.instance(peewee.Database),
                             inject.instance(config_loader.ConfigLoader).get_article('guard_connect')))
    binder.bind_to_constructor(rep.DriverConnection,
        lambda: DBFromConfig(inject.instance(peewee.Database),
                             inject.instance(config_loader.ConfigLoader).get_article('driver_connect')))
    binder.bind_to_constructor(rep.UnverifConnection,
        lambda: DBFromConfig(inject.instance(peewee.Database),
                             inject.instance(config_loader.ConfigLoader).get_article('unverif_connect')))


def inject_config_rep(binder):
    binder.bind(PersonRepository, PWPersonRep)
    binder.bind(AccountsRepository, PWAccountsRep)
    binder.bind(TrucksRepository, PWTrucksRep)
    binder.bind(CheckpointsRepository, PWCheckpointsRep)
    binder.bind(DeliveryRepository, PWDeliveryRep)
    binder.bind(DriverDutyRepository, PWDriverDutyRep)
    binder.bind(GuardDutyRepository, PWGuardDutyRep)
    binder.bind(PassRecordsRepository, PWPassRecordsRep)


def inject_config(binder):
    inject_config_db(binder)
    inject_config_rep(binder)


print('#' * 30)
inject.clear_and_configure(inject_config)
print('!' * 30)
