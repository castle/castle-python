class ContextSanitizer(object):

    @classmethod
    def call(cls, context):
        sanitized_context = cls._sanitize_active_mode(context)
        if sanitized_context:
            return sanitized_context
        return dict()

    @classmethod
    def _sanitize_active_mode(cls, context):
        if context is None:
            return None
        elif 'active' not in context:
            return context
        elif isinstance(context.get('active'), bool):
            return context

        context_copy = context.copy()
        context_copy.pop('active')
        return context_copy
