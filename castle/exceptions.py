# All exceptions should subclass from CastleError in this module.
class CastleError(Exception):
    """Base class for all Castle errors."""

# Raised when invalid failover strategy value passed
class FailoverStrategyValueError(CastleError):
    pass

# Raised when invalid parameter are passed
class InvalidParametersError(CastleError):
    pass

class BadRequestError(CastleError):
    pass

class UnauthorizedError(CastleError):
    pass

class ForbiddenError(CastleError):
    pass

class NotFoundError(CastleError):
    pass

class UserUnauthorizedError(CastleError):
    pass

class ApiError(CastleError):
    pass

class InternalServerError(CastleError):
    pass
