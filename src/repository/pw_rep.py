from src.repository.repository import AbstractDB
from peewee import *
import inject


def request_to_objects(req, obj_class):
    obj_arr = []
    for obj_dict in req.dicts():
        obj_arr.append(obj_class(obj_dict))
    return obj_arr


class BaseModel(Model):
    class Meta:
        database = inject.instance(AbstractDB)


class AccountsModel(BaseModel):
    login = TextField(column_name='login', primary_key=True)
    perstype = TextField(column_name='perstype', null=False)
    salt = TextField(column_name='salt', null=False)
    hashedpassword = TextField(column_name='hashedpassword', null=False)

    class Meta:
        table_name = 'accounts'
