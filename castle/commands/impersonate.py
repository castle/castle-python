from castle.command import Command
from castle.utils.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.merge import ContextMerge
from castle.context.sanitize import ContextSanitize
from castle.validators.present import ValidatorsPresent


class CommandsImpersonate(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsPresent.call(options, 'user_id')

        context = ContextMerge.call(self.context, options.get('context'))
        context = ContextSanitize.call(context)
        ValidatorsPresent.call(context, 'user_agent', 'ip')

        if context:
            options.update({'context': context})
        options.update({'sent_at': generate_timestamp.call()})

        method = ('delete' if options.get('reset', False) else 'post')

        return Command(method=method, path='impersonate', data=options)
