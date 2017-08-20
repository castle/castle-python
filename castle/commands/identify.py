from castle.command import Command
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsIdentify(object):
    def __init__(self, context):
        self.context_merger = ContextMerger(context)

    def build(self, options):
        user_id = options.get('user_id')
        if user_id is None or user_id == '':
            raise InvalidParametersError

        args = {
            'user_id': user_id,
            'context': self.build_context(options.get('context', dict()))
        }

        if 'active' in options and options['active']:
            args['active'] = True
        if 'traits' in options:
            args['traits'] = options['traits']

        return Command(method='post', endpoint='identify', data=args)

    def build_context(self, context):
        return self.context_merger.call(context or {})
