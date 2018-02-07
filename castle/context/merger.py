from castle.utils import clone, deep_merge


class ContextMerger(object):

    @staticmethod
    def call(initial_context, request_context):
        source_copy = clone(initial_context)
        deep_merge(source_copy, request_context)
        return source_copy
