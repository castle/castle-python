from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsListsCreate(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'name', 'color', 'primary_field')

        return Command(method='post', path='lists', data=options)
