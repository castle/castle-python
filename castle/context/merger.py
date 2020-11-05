from castle.utils2.merge import UtilsMerge
from castle.utils2.clone import UtilsClone


class ContextMerger(object):

    @staticmethod
    def call(initial_context, request_context):
        source_copy = UtilsClone.call(initial_context)
        UtilsMerge.call(source_copy, request_context)
        return source_copy
