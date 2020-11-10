import enum


# handles verdict consts
class Verdict(enum.Enum):
    # allow
    ALLOW = 'allow'
    # challenge
    CHALLENGE = 'challenge'
    # deny
    DENY = 'deny'
