import copy

class UtilsClone(object):

    @staticmethod
    def call(dict_object):
        return copy.deepcopy(dict_object)
