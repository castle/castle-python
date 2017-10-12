from castle.command import Command
from castle.commands.with_context import validate, WithContext
from castle.exceptions import InvalidParametersError


class CommandsIdentify(WithContext):
    def build(self, options):
        validate(options, 'user_id')

        if options.get('properties'):
            raise InvalidParametersError('properties are not supported in identify calls')

        return Command(method='post', endpoint='identify', data=self.build_context(options))
