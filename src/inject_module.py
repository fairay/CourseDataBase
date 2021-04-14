import inject
import peewee
import config_loader
from src.repository import repository as rep

def inject_config0(binder):
    binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('config.json'))
    binder.bind_to_constructor(rep.AbstractDB, lambda: DBFromConfig(inject.instance(peewee.Database),
                                                                    inject.instance(config_loader.ConfigLoader)))
inject.configure(inject_config0)

from src.repository import pers_rep
from src.repository.pw_db import DBFromConfig
from src.repository.acc_rep import AccountsRepository, PWAccountsRep

def inject_config(binder):
    binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('config.json'))
    binder.bind_to_constructor(rep.AbstractDB, lambda: DBFromConfig(inject.instance(config_loader.ConfigLoader)))

    binder.bind_to_constructor(pers_rep.PersonRepository, lambda: pers_rep.PWPersonRep())
    binder.bind_to_constructor(AccountsRepository, lambda: PWAccountsRep())


# inject.configure(inject_config)
inject.clear_and_configure(inject_config)


def main():
    person = inject.instance(pers_rep.PersonRepository)  # pers_rep.PWPersonRep()
    print(person)
    pers_arr = person.ready()
    print(pers_arr)


if __name__ == '__main__':
    main()
