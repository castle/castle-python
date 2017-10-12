from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


def validate(options, *args):
    for key in args:
        if options.get(key) is None or options.get(key) == '':
            raise InvalidParametersError("{key} is missing or empty".format(key=key))

def sanitize_active_mode(options):
    if 'active' in options.get('context', dict()):
        if not isinstance(options.get('context').get('active'), bool):
            del options['context']['active']


class WithContext(object):
    def __init__(self, context):
        self.context_merger = ContextMerger(context)

    def build_context(self, options):
        sanitize_active_mode(options)
        options['context'] = self.merge_context(options.get('context', dict()))
        return options

    def merge_context(self, context):
        return self.context_merger.call(context)
