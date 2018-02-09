from castle.exceptions import InvalidParametersError


class ValidatorsNotSupported(object):

    @staticmethod
    def call(options, *args):
        for key in args:
            if key in options:
                raise InvalidParametersError(
                    "{key} is not supported".format(key=key))
