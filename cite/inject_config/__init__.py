import inject
import peewee
from playhouse.postgres_ext import *
import config_loader
import repository.repository as rep
from repository.pw_db import DBFromConfig


def inject_config0(binder):
    binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('config.json'))

    binder.bind_to_constructor(rep.AbstractConnection,
        lambda: DBFromConfig(inject.instance(peewee.Database),
                             inject.instance(config_loader.ConfigLoader).get_article('admin_connect')))
    binder.bind_to_constructor(rep.TestConnection,
        lambda: PostgresqlExtDatabase('peewee_unittest', user='admin'))
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


print('!' * 30)
inject.clear_and_configure(inject_config0)

from repository.pers_rep import PersonRepository, PWPersonRep
from repository.acc_rep import AccountsRepository, PWAccountsRep
from repository.truck_rep import TrucksRepository, PWTrucksRep

def inject_config(binder):
    inject_config0(binder)

    binder.bind(PersonRepository, PWPersonRep)
    # TODO: remove inject.instance(AbstractConnection)
    binder.bind(AccountsRepository, PWAccountsRep)
    binder.bind(TrucksRepository, PWTrucksRep)


print('#' * 30)
inject.clear_and_configure(inject_config)
