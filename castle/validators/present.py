from castle.exceptions import InvalidParametersError


class ValidatorsPresent(object):

    @staticmethod
    def call(options, *args):
        for key in args:
            if options.get(key) is None or options.get(key) == '':
                raise InvalidParametersError(
                    "{key} is missing or empty".format(key=key))
