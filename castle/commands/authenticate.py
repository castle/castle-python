from castle.command import Command
from castle.context import ContextMerger, ContextSanitizer
from castle.validators import ValidatorsPresent


class CommandsAuthenticate(object):
    def __init__(self, context):
        self.context = context

    def build(self, options):
        ValidatorsPresent.call(options, 'event', 'user_id')
        context = ContextMerger.call(self.context, options['context'])
        context = ContextSanitizer.call(context)
        options.update({'sent_at': timestamp(), 'context': context})

        return Command(method='post', path='authenticate', data=options)



