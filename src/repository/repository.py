class Repository(object):
    def __init__(self):
        pass

    def create(self, obj):
        raise NotImplemented

    def delete(self, obj):
        raise NotImplemented

    def update(self, obj):
        raise NotImplemented

    def get(self):
        raise NotImplemented


class AbstractDB(object):
    pass
