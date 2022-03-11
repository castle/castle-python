class UtilsMerge(object):

    @classmethod
    def call(cls, base, extra):
        """
        Deeply merge two dictionaries, overriding existing keys in the base.

        :param base: The base dictionary which will be merged into.
        :param extra: The dictionary to merge into the base. Keys from this
            dictionary will take precedence.
        """
        if extra is None or base is None:
            return

        for key, value in extra.items():
            if value is None:
                if key in base:
                    del base[key]
            # If the key represents a dict on both given dicts, merge the sub-dicts
            elif isinstance(base.get(key), dict) and isinstance(value, dict):
                cls.call(base[key], value)
            else:
                # Otherwise, set the key on the base to be the value of the extra.
                base[key] = value
