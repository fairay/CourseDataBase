class ConfigMissingExc(BaseException): pass


class RepositoryExc(BaseException): pass
class ObjectCreateExc(RepositoryExc): pass
class AlreadyExistsExc(RepositoryExc): pass
class WrongUpdExc(RepositoryExc): pass
class NullValExc(RepositoryExc): pass


class AccountExc(BaseException): pass
class NotAuthorisedExc(AccountExc): pass
class NotAllowedExc(AccountExc): pass
class UnverifiedExc(AccountExc): pass
class VerifiedExc(AccountExc): pass
class NonExistentExc(AccountExc): pass
class UnknownRoleExc(AccountExc): pass
