class ConfigMissingExc(BaseException): pass


class RepositoryExc(BaseException): pass
class ObjectCreateExc(RepositoryExc): pass
class AlreadyExistsExc(RepositoryExc): pass
class NotExistsExc(RepositoryExc): pass
class WrongUpdExc(RepositoryExc): pass
class NullValExc(RepositoryExc): pass


class AccountExc(BaseException): pass
class NotAuthorisedExc(AccountExc): pass
class NotAllowedExc(AccountExc): pass
class UnverifiedExc(AccountExc): pass
class VerifiedExc(AccountExc): pass
class NonExistentExc(AccountExc): pass
class UnknownRoleExc(AccountExc): pass


class CreateObjExc(BaseException): pass
class LackArgExc(CreateObjExc): pass
class WrongFormatExc(CreateObjExc): pass


class TruckExc(BaseException): pass
class TruckLackExc(TruckExc): pass
class TruckWrongExc(TruckExc): pass


class CheckpointExc(BaseException): pass
class CheckpointLackExc(CheckpointExc): pass
class CheckpointWrongExc(CheckpointExc): pass


class DeliveryExc(BaseException): pass
class DeliveryWrongExc(DeliveryExc): pass
