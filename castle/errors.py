# All errors should subclass from CastleError in this module.
class CastleError(Exception):
    """Base class for all Castle errors."""


class RequestError(CastleError):
    pass


class SecurityError(CastleError):
    pass


class ConfigurationError(CastleError):
    pass


class APIError(CastleError):
    pass


class InvalidParametersError(APIError):
    pass


class BadRequestError(APIError):
    pass


class UnauthorizedError(APIError):
    pass


class UserUnauthorizedError(APIError):
    pass


class ForbiddenError(APIError):
    pass


class NotFoundError(APIError):
    pass


class InternalServerError(APIError):
    pass


class ImpersonationFailed(APIError):
    pass
