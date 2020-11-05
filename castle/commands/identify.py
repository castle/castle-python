from castle.command import Command
from castle.utils.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.merge import ContextMerge
from castle.context.sanitize import ContextSanitize
from castle.validators.not_supported import ValidatorsNotSupported


class CommandsIdentify(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsNotSupported.call(options, 'properties')
        context = ContextMerge.call(self.context, options.get('context'))
        context = ContextSanitize.call(context)
        if context:
            options.update({'context': context})
        options.update({'sent_at': generate_timestamp.call()})

        return Command(method='post', path='identify', data=options)
