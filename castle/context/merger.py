from castle.utils import clone, deep_merge


class ContextMerger(object):
    def __init__(self, source):
        self.source_copy = clone(source)

    def call(self, context):
        deep_merge(self.source_copy, context)
        return self.source_copy
