from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListItemsCreateBatch(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'list_id', 'items')

        list_id = options.pop('list_id')

        return Command(
            method='post', path='lists/{list_id}/items/batch'.format(list_id=list_id), data=options
        )
