from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsPrivacyDeleteData(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'identifier', 'identifier_type')

        return Command(method='delete', path='privacy/users', data=options)
