from peewee import *
import inject


# class DBFromConfig(inject.instance(Database)):
#    def __init__(self, config):
def DBFromConfig(db_class, config):
        db_name = config.get_article('db_name')
        db_user = config.get_article('db_user')
        db_password = config.get_article('db_password')
        db_host = config.get_article('db_host')

        return db_class(db_name, user=db_user, password=db_password, host=db_host)
