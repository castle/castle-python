from castle.command import Command
from castle.context import ContextMerger, ContextSanitizer
from castle.validators import ValidatorsPresent, ValidatorsNotSupported


class CommandsIdentify(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsPresent.call(options, 'user_id')
        ValidatorsNotSupported.call(options, 'properties')
        context = ContextMerger.call(self.context, options['context'])
        context = ContextSanitizer.call(context)
        options.update({'sent_at': timestamp(), 'context': context})

        return Command(method='post', path='identify', data=options)

