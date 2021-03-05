from castle.command import Command
from castle.utils.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.merge import ContextMerge
from castle.context.sanitize import ContextSanitize
from castle.validators.present import ValidatorsPresent


class CommandsEndImpersonation(object):
    def __init__(self, context):
        self.context = context

    def call(self, options):
        ValidatorsPresent.call(options, 'user_id')

        context = ContextMerge.call(self.context, options.get('context'))
        context = ContextSanitize.call(context)
        ValidatorsPresent.call(context, 'ip')

        if context:
            options.update({'context': context})
        options.update({'sent_at': generate_timestamp.call()})

        return Command(method='delete', path='impersonate', data=options)
