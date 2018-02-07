import copy
from datetime import datetime

def clone(dict_object):
    return copy.deepcopy(dict_object)


def deep_merge(base, extra):
    """
    Deeply merge two dictionaries, overriding existing keys in the base.

    :param base: The base dictionary which will be merged into.
    :param extra: The dictionary to merge into the base. Keys from this
        dictionary will take precedence.
    """
    for key, value in extra.items():
        # If the key represents a dict on both given dicts, merge the sub-dicts
        if value is None:
          del base[key]
        elif isinstance(base[key], dict) and isinstance(value, dict):
          deep_merge(base[key], value)
        else:
           # Otherwise, set the key on the base to be the value of the extra.
          base[key] = extra[key]


def timestamp():
    """Return an ISO8601 timestamp representing the current datetime in UTC."""
    return datetime.utcnow().isoformat()[:-3]

