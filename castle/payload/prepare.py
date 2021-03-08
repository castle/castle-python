import warnings

from castle.utils.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.prepare import ContextPrepare
from castle.options.get_default import OptionsGetDefault
from castle.options.merge import OptionsMerge


class PayloadPrepare(object):

    @staticmethod
    def call(payload_options, request, options=None):
        if options is None:
            options = {}

        default_options = OptionsGetDefault(request, options.get('cookies')).call()
        options_with_default_opts = OptionsMerge.call(options, default_options)
        options_for_payload = OptionsMerge.call(payload_options, options_with_default_opts)

        context = ContextPrepare.call(options_for_payload)

        options_for_payload.setdefault('context', context)
        options_for_payload.setdefault('timestamp', generate_timestamp.call())

        if 'traits' in options_for_payload:
            warnings.warn('use user_traits instead of traits key', DeprecationWarning)

        return options_for_payload
