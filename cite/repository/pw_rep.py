from repository.repository import AbstractConnection
from peewee import *
import inject


def request_to_objects(req, obj_class):
    obj_arr = []
    for obj_dict in req.dicts():
        obj_arr.append(obj_class(**obj_dict))
    return obj_arr


class BaseModel(Model):
    def __init__(self, con: Database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.database = con


class AccountsModel(BaseModel):
    login = TextField(column_name='login', primary_key=True)
    perstype = TextField(column_name='perstype', null=False)
    salt = TextField(column_name='salt', null=False)
    hashedpassword = TextField(column_name='hashedpassword', null=False)

    class Meta:
        table_name = 'accounts'


class PersonModel(BaseModel):
    login = ForeignKeyField(AccountsModel, column_name='login', primary_key=True)
    surname = CharField(column_name='surname', max_length=40, null=False)
    forename = CharField(column_name='forename', max_length=40, null=False)
    dob = DateField(column_name='dob', null=False)
    gender = FixedCharField(column_name='gender', max_length=1, null=False)
    phonenumber = TextField(column_name='phonenumber')

    class Meta:
        table_name = 'person'
