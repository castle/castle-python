from castle.utils import clone, merge

class ContextMerger(object):
    def __init__(self, source):
        self.source_copy = clone(source)

    def call(self, context):
        return merge(self.source_copy, context)
