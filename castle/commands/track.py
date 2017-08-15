from castle.command import Command
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsTrack(object):
    def initialize(self, context):
        self.context_merger = ContextMerger(context)

    def build(self, options):
        event = options['event']
        if event is None or event == '':
            raise InvalidParametersError

        args = {
            'event': event,
            'context': self.build_context(options['context'])
        }

        if 'user_id' in options:
            args['user_id'] = options['user_id']
        if 'properties' in options:
            args['properties'] = options['properties']

        return Command(method='post', endpoint='track', data=args)

    def build_context(self, context):
        self.context_merger.call(context or {})
