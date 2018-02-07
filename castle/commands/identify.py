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
        ValidatorsPresent.call(options, 'user_id')
        ValidatorsNotSupported.call(options, 'properties')
        context = ContextMerger.call(self.context, options['context'])
        context = ContextSanitizer.call(context)
        options.update({'sent_at': timestamp(), 'context': context})

        return Command(method='post', path='identify', data=options)
