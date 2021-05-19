class Repository(object):
    def __init__(self, con):
        pass

    def create(self, obj):
        raise NotImplementedError

    def delete(self, obj):
        raise NotImplementedError

    def update(self, old_obj, new_obj):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError


class AbstractConnection(object): pass
class TestConnection(AbstractConnection):
    def __repr__(self): return 'test'
class AdminConnection(AbstractConnection):
    def __repr__(self): return 'admin'
class GuardConnection(AbstractConnection):
    def __repr__(self): return 'guard'
class DriverConnection(AbstractConnection):
    def __repr__(self): return 'driver'
class UnverifConnection(AbstractConnection):
    def __repr__(self): return '~'


con_dict = {}
for cl in AbstractConnection.__subclasses__():
    con_dict[str(cl())] = cl
