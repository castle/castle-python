# All exceptions should subclass from CastleError in this module.
class CastleError(Exception):
    """Base class for all Castle errors."""

# Raised when invalid failover strategy value passed
class FailoverStrategyValueError(CastleError):
    pass

# Raised when invalid parameter are passed
class InvalidParametersError(CastleError):
    pass
