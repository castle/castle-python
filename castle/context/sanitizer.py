from castle.utils import clone, deep_merge


class ContextSanitizer(object):

    @classmethod
    def call(self, context):
        sanitized_context = self._sanitize_active_mode(context)
        if sanitized_context:
          return sanitized_context
        else:
          return dict()

    @staticmethod
    def _sanitize_active_mode(context):
        if not context:
            return
        elif 'active' not in context:
            return context
        elif isinstance(context.get('active'), bool):
            return context
        else:
            context_copy = context.copy()
            context_copy.pop('active')
            return context_copy;


