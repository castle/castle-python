from castle.command import Command
from castle.utils.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.merge import ContextMerge
from castle.context.sanitize import ContextSanitize


class CommandsRisk(object):
    def __init__(self, context):
        self.context = context

    def call(self, options):
        context = ContextMerge.call(self.context, options.get('context'))
        context = ContextSanitize.call(context)
        if context:
            options.update({'context': context})
        options.update({'sent_at': generate_timestamp.call()})

        return Command(method='post', path='risk', data=options)
