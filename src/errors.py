class RepositoryExc(BaseException): pass


class ObjectCreateExc(RepositoryExc): pass
class AlreadyExistsExc(RepositoryExc): pass
class WrongUpdExc(RepositoryExc): pass
class NullValExc(RepositoryExc): pass
