from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsPrivacyRequestData(object):
    @staticmethod
    def call(options=None):
        options = options or {}
        ValidatorsPresent.call(options, 'identifier', 'identifier_type')

        return Command(method='post', path='privacy/users', data=options)
