from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListsUpdate(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'list_id')

        list_id = options.pop('list_id')

        return Command(method='put', path='lists/{list_id}'.format(list_id=list_id), data=options)
