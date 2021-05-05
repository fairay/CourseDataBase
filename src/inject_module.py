import inject
import peewee
from src import config_loader
from src.repository import repository as rep
from src.repository.pw_db import DBFromConfig
import os

def inject_config0(binder):
    os.path.join(os.path.dirname(os.path.dirname(__file__)))
    binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('..\\src\\config.json'))
    binder.bind_to_constructor(rep.AbstractConnection, lambda: DBFromConfig(inject.instance(peewee.Database),
                                                                            inject.instance(config_loader.ConfigLoader)))


inject.configure(inject_config0)


from src.repository.pers_rep import PersonRepository, PWPersonRep
from src.repository.acc_rep import AccountsRepository, PWAccountsRep


def inject_config(binder):
    inject_config0(binder)

    binder.bind_to_constructor(PersonRepository, lambda: PWPersonRep())
    binder.bind_to_constructor(AccountsRepository, lambda: PWAccountsRep())


# inject.configure(inject_config)
inject.clear_and_configure(inject_config)


def main():
    person = inject.instance(PersonRepository)  # pers_rep.PWPersonRep()
    print(person)
    pers_arr = person.ready()
    print(pers_arr)


if __name__ == '__main__':
    main()
