from castle.context.get_default import ContextGetDefault
from castle.context.merge import ContextMerge


class ContextPrepare(object):

    @staticmethod
    def call(options=None):
        if options is None:
            options = {}
        default_context = ContextGetDefault.call()
        return ContextMerge.call(default_context, options.get('context', {}))
