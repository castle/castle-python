import enum


# handles verdict consts
class Verdict(enum.Enum):
    # allow
    ALLOW = 'allow'
    # deny
    DENY = 'deny'
    # challenge
    CHALLENGE = 'challenge'
