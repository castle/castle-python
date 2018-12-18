from castle.command import Command
from castle.utils import timestamp
from castle.context.merger import ContextMerger
from castle.context.sanitizer import ContextSanitizer
from castle.validators.present import ValidatorsPresent


class CommandsImpersonate(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsPresent.call(options, 'user_id')

        context = ContextMerger.call(self.context, options.get('context'))
        context = ContextSanitizer.call(context)
        ValidatorsPresent.call(context, 'user_agent', 'ip')

        if context:
            options.update({'context': context})
        options.update({'sent_at': timestamp()})

        method = ('delete' if options.get('reset', False) else 'post')

        return Command(method=method, path='impersonate', data=options)
