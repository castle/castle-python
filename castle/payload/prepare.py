import warnings

from castle.utils.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.prepare import ContextPrepare
from castle.utils.merge import UtilsMerge


class PayloadPrepare(object):

    @staticmethod
    def call(payload_options, request, options=None):
        if options is None:
            options = {}

        context = ContextPrepare.call(request, UtilsMerge.call(payload_options, options))

        payload_options.setdefault('context', context)
        payload_options.setdefault('timestamp', generate_timestamp.call())

        if 'traits' in payload_options:
            warnings.warn('use user_traits instead of traits key', DeprecationWarning)

        return payload_options
