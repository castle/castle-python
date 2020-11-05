from castle.command import Command
from castle.utils2.timestamp import UtilsTimestamp as generate_timestamp
from castle.context.merger import ContextMerger
from castle.context.sanitizer import ContextSanitizer
from castle.validators.present import ValidatorsPresent


class CommandsAuthenticate(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsPresent.call(options, 'event')
        context = ContextMerger.call(self.context, options.get('context'))
        context = ContextSanitizer.call(context)
        if context:
            options.update({'context': context})
        options.update({'sent_at': generate_timestamp.call()})

        return Command(method='post', path='authenticate', data=options)
