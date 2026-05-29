from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListsGet(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'list_id')

        return Command(
            method='get', path='lists/{list_id}'.format(list_id=options['list_id']), data=None
        )
