from repository import *
from peewee import *
import inject


class DBFromConfig(inject.instance(Database)):
    def __init__(self, config):
        db_name = config.get_article('db_name')
        db_user = config.get_article('db_user')
        db_password = config.get_article('db_password')
        db_host = config.get_article('db_host')

        super(DBFromConfig, self).__init__(db_name, user=db_user, password=db_password, host=db_host)


class BaseModel(Model):
    class Meta:
        database = inject.instance(AbstractDB)


class AccountsModel(BaseModel):
    Login = TextField(column_name='login', primary_key=True)
    PersType = TextField(column_name='perstype', null=False)
    Salt = TextField(column_name='salt', null=False)
    HashedPassword = TextField(column_name='hashedpassword', null=False)

    class Meta:
        table_name = 'accounts'
