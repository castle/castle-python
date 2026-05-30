from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListItemsUpdate(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'list_id', 'list_item_id', 'comment')

        list_id = options.pop('list_id')
        list_item_id = options.pop('list_item_id')

        return Command(
            method='put',
            path='lists/{list_id}/items/{list_item_id}'.format(
                list_id=list_id, list_item_id=list_item_id
            ),
            data=options,
        )
