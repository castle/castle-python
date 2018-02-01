import copy
from datetime import datetime

import pytz


def clone(dict_object):
    return copy.deepcopy(dict_object)


def deep_merge(base, extra):
    """
    Deeply merge two dictionaries, overriding existing keys in the base.

    :param base: The base dictionary which will be merged into.
    :param extra: The dictionary to merge into the base. Keys from this
        dictionary will take precedence.
    """
    for key in extra.iterkeys():
        # If the key represents a dict on both given dicts, merge the sub-dicts
        if key in base and isinstance(base[key], dict)\
                and isinstance(extra[key], dict):
            deep_merge(base[key], extra[key])
            continue

        # Otherwise, set the key on the base to be the value of the extra.
        base[key] = extra[key]


def timestamp():
    """Return an ISO8601 timestamp representing the current datetime in UTC."""
    return datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
