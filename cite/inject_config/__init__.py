import inject
import peewee
import config_loader
import repository.repository as rep
from repository.pw_db import DBFromConfig


def inject_config0(binder):
    binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('config.json'))
    binder.bind_to_constructor(rep.AbstractConnection, lambda: DBFromConfig(inject.instance(peewee.Database),
                                                                            inject.instance(
                                                                                config_loader.ConfigLoader)))

print('!' * 30)
inject.clear_and_configure(inject_config0)

from repository.pers_rep import PersonRepository, PWPersonRep
from repository.acc_rep import AccountsRepository, PWAccountsRep


def inject_config(binder):
    inject_config0(binder)

    binder.bind_to_constructor(PersonRepository, lambda: PWPersonRep())
    binder.bind_to_constructor(AccountsRepository, lambda: PWAccountsRep())

print('#' * 30)
inject.clear_and_configure(inject_config)