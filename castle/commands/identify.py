from castle.command import Command
from castle.utils import timestamp
from castle.context.merger import ContextMerger
from castle.context.sanitizer import ContextSanitizer
from castle.validators.present import ValidatorsPresent
from castle.validators.not_supported import ValidatorsNotSupported


class CommandsIdentify(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsNotSupported.call(options, 'properties')
        context = ContextMerger.call(self.context, options.get('context'))
        context = ContextSanitizer.call(context)
        if context:
            options.update({'context': context})
        options.update({'sent_at': timestamp()})

        return Command(method='post', path='identify', data=options)
