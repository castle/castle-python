import enum


# handles failover strategy consts
class FailoverStrategy(enum.Enum):
    # allow
    ALLOW = 'allow'
    # challenge
    CHALLENGE = 'challenge'
    # deny
    DENY = 'deny'
    # throw an error
    THROW = 'throw'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
