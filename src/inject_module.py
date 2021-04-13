import inject
import peewee
inject.configure(lambda bld: bld.bind(peewee.Database, peewee.PostgresqlDatabase))

from src.repository import repository as rep, pers_rep
from src.repository.pw_rep import DBFromConfig
from src.repository.acc_rep import AccountsRepository, PWAccountsRep
import config_loader


def inject_config(binder):
    # binder.bind(peewee.Database, peewee.PostgresqlDatabase)
    binder.bind_to_constructor(config_loader.ConfigLoader, lambda: config_loader.ConfigLoader('config.json'))
    binder.bind_to_constructor(rep.AbstractDB, lambda: DBFromConfig(inject.instance(config_loader.ConfigLoader)))

    binder.bind_to_constructor(pers_rep.PersonRepository, lambda: pers_rep.PWPersonRep())
    binder.bind_to_constructor(AccountsRepository, lambda: PWAccountsRep())


inject.configure(inject_config)


def main():
    person = inject.instance(pers_rep.PersonRepository)  # pers_rep.PWPersonRep()
    print(person)
    pers_arr = person.ready()
    print(pers_arr)


if __name__ == '__main__':
    main()
