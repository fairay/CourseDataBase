class Repository(object):
    def __init__(self):
        pass

    def create(self, object):
        raise NotImplemented

    def delete(self, object):
        raise NotImplemented

    def update(self, object):
        raise NotImplemented

    def get(self):
        raise NotImplemented


class AbstractDB(object):
    def __init__(self):
        do_a = 'burrell roll'
