from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListItemsCount(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'list_id')
        for query_filter in options.get('filters') or []:
            ValidatorsPresent.call(query_filter, 'field', 'op', 'value')

        list_id = options.pop('list_id')

        return Command(
            method='post', path='lists/{list_id}/items/count'.format(list_id=list_id), data=options
        )
