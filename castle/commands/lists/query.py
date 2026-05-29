from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListsQuery(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        for query_filter in options.get('filters') or []:
            ValidatorsPresent.call(query_filter, 'field', 'op', 'value')
        if options.get('sort'):
            ValidatorsPresent.call(options['sort'], 'field', 'order')

        return Command(method='post', path='lists/query', data=options)
