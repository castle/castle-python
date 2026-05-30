from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListItemsGet(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'list_id', 'list_item_id')

        return Command(
            method='get',
            path='lists/{list_id}/items/{list_item_id}'.format(
                list_id=options['list_id'], list_item_id=options['list_item_id']
            ),
            data=None,
        )
