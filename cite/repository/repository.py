class Repository(object):
    def create(self, obj):
        raise NotImplementedError

    def delete(self, obj):
        raise NotImplementedError

    def update(self, old_obj, new_obj):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError


class AbstractConnection(object): pass
class TestConnection(AbstractConnection): pass
class AdminConnection(AbstractConnection): pass
class GuardConnection(AbstractConnection): pass
class DriverConnection(AbstractConnection): pass
class UnverifConnection(AbstractConnection): pass
