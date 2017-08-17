from castle.command import Command
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsAuthenticate(object):
    def __init__(self, context):
        self.context_merger = ContextMerger(context)

    def build(self, options):
        event = options['event']
        if event is None or event == '':
            raise InvalidParametersError

        user_id = options['user_id']
        if user_id is None or user_id == '':
            raise InvalidParametersError

        args = {
            # TODO: rename back to event
            'name': event,
            'user_id': user_id,
            'context': self.build_context(options.get('context', dict()))
        }

        if 'properties' in options:
            args['properties'] = options['properties']

        return Command(method='post', endpoint='authenticate', data=args)

    def build_context(self, context):
        return self.context_merger.call(context)
