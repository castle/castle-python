from castle.utils.merge import UtilsMerge
from castle.utils.clone import UtilsClone


class OptionsMerge(object):

    @staticmethod
    def call(initial_options, request_options):
        source_copy = UtilsClone.call(initial_options)
        UtilsMerge.call(source_copy, request_options)
        return source_copy
