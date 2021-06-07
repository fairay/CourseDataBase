from repository.repository import AbstractConnection
from peewee import *
import inject


def storedf_call(con: Database, f_name, *f_args):
    cur = con.cursor()
    cur.callproc(f_name, f_args)

    query_res = []
    for obj in cur.fetchall():
        obj_dict = {}
        for col, val in zip(cur.description, obj):
            col_name = col[0]
            obj_dict[col_name] = val
        query_res.append(obj_dict)
    cur.close()

    return query_res


def request_to_objects(req, obj_class):
    obj_arr = []
    for obj_dict in req.dicts():
        obj_arr.append(obj_class(**obj_dict))
    return obj_arr


def dicts_to_objects(dict_arr: [dict], obj_class):
    obj_arr = []
    for obj_dict in dict_arr:
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


class CheckpointsModel(BaseModel):
    checkpointid = AutoField(column_name='checkpointid', primary_key=True)
    address = TextField(column_name='address', null=False)
    phonenumber = CharField(column_name='phonenumber', max_length=40, null=False)

    class Meta:
        table_name = 'checkpoints'


class TrucksModel(BaseModel):
    platenumber = TextField(column_name='platenumber', primary_key=True)
    category = CharField(column_name='category', max_length=40, null=False)
    model = CharField(column_name='model', max_length=40, null=False)

    class Meta:
        table_name = 'trucks'


class DeliveryModel(BaseModel):
    orderid = AutoField(column_name='orderid', primary_key=True)
    login = ForeignKeyField(AccountsModel, column_name='login', null=True)
    address = TextField(column_name='address', null=False)
    phonenumber = CharField(column_name='phonenumber', max_length=40, null=False)
    creationtime = DateTimeField(column_name='creationtime', null=False)
    completiontime = DateTimeField(column_name='completiontime', null=True)
    status = CharField(column_name='status', max_length=20, null=False)
    description = TextField(column_name='description', null=False)

    class Meta:
        table_name = 'delivery'


class PassRecordsModel(BaseModel):
    recordid = AutoField(column_name='recordid', primary_key=True)
    platenumber = ForeignKeyField(TrucksModel, column_name='platenumber', null=False)
    checkpointid = ForeignKeyField(CheckpointsModel, column_name='checkpointid', null=False)
    passtime = DateTimeField(column_name='passtime', null=False)
    direction = CharField(column_name='direction', max_length=3, null=False,
                          constraints=[Check("(direction='in' OR direction='out')")])

    class Meta:
        table_name = 'passrecords'


class GuardDutysModel(BaseModel):
    dutyid = AutoField(column_name='dutyid', primary_key=True)
    checkpointid = ForeignKeyField(CheckpointsModel, column_name='checkpointid', null=False)
    login = ForeignKeyField(AccountsModel, column_name='login', null=False)
    begindate = DateField(column_name='begindate', null=False)
    enddate = DateField(column_name='enddate', null=True)
    begintime = TimeField(column_name='begintime', null=False)
    endtime = TimeField(column_name='endtime', null=False)
    dow = CharField(column_name='dow', max_length=7, null=False)

    class Meta:
        table_name = 'guarddutys'


class DriverDutysModel(BaseModel):
    dutyid = AutoField(column_name='dutyid', primary_key=True)
    platenumber = ForeignKeyField(TrucksModel, column_name='platenumber', null=False)
    login = ForeignKeyField(AccountsModel, column_name='login', null=False)
    begindate = DateField(column_name='begindate', null=False)
    enddate = DateField(column_name='enddate', null=True)
    begintime = TimeField(column_name='begintime', null=False)
    endtime = TimeField(column_name='endtime', null=False)
    dow = CharField(column_name='dow', max_length=7, null=False)

    class Meta:
        table_name = 'driverdutys'


class DutyRulesModel(BaseModel):
    ruleid = AutoField(column_name='ruleid', primary_key=True)
    begindate = DateField(column_name='begindate', null=False)
    enddate = DateField(column_name='enddate', null=True)
    begintime = TimeField(column_name='begintime', null=False)
    endtime = TimeField(column_name='endtime', null=False)
    dow = CharField(column_name='dow', max_length=7, null=False)

    class Meta:
        table_name = 'dutyrules'


class GuardRDutyModel(BaseModel):
    dutyid = AutoField(column_name='dutyid', primary_key=True)
    checkpointid = ForeignKeyField(CheckpointsModel, column_name='checkpointid', null=False)
    login = ForeignKeyField(AccountsModel, column_name='login', null=False)
    ruleid = ForeignKeyField(DutyRulesModel, column_name='ruleid', null=False)

    class Meta:
        table_name = 'guardduty'


class DriverRDutyModel(BaseModel):
    dutyid = AutoField(column_name='dutyid', primary_key=True)
    platenumber = ForeignKeyField(TrucksModel, column_name='platenumber', null=False)
    login = ForeignKeyField(AccountsModel, column_name='login', null=False)
    ruleid = ForeignKeyField(DutyRulesModel, column_name='ruleid', null=False)

    class Meta:
        table_name = 'driverduty'
