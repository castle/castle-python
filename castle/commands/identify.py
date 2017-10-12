from castle.command import Command
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsIdentify(object):
    def __init__(self, context):
        self.context_merger = ContextMerger(context)

    def build(self, options):
        self.validate(options)

        if 'active' in options.get('context', dict()):
            if not isinstance(options.get('context').get('active'), bool):
                del options['context']['active']

        args = {
            'user_id': options['user_id'],
            'context': self.build_context(options.get('context', dict()))
        }

        if 'traits' in options:
            args['traits'] = options['traits']

        return Command(method='post', endpoint='identify', data=args)

    def validate(self, options):
        for key in ['user_id']:
            if options.get(key) is None or options.get(key) == '':
                raise InvalidParametersError("{key} is missing or empty".format(key=key))

    def build_context(self, context):
        return self.context_merger.call(context or {})
