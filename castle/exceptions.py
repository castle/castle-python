# All exceptions should subclass from CastleError in this module.
class CastleError(Exception):
    """Base class for all Castle errors."""


class RequestError(CastleError):
    pass

class SecurityError(CastleError):
    pass

class ConfigurationError(CastleError):
    pass

class ApiError(CastleError):
    pass


class InvalidParametersError(ApiError):
    pass

class BadRequestError(ApiError):
    pass

class UnauthorizedError(ApiError):
    pass

class UserUnauthorizedError(ApiError):
    pass

class ForbiddenError(ApiError):
    pass

class NotFoundError(ApiError):
    pass

class InternalServerError(ApiError):
    pass

class ImpersonationFailed(ApiError):
    pass
