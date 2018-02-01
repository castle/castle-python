from castle.command import Command
from castle.commands.with_context import validate, WithContext
from castle.exceptions import InvalidParametersError
from castle.utils import timestamp


class CommandsIdentify(WithContext):
    def build(self, options):
        validate(options, 'user_id')
        options.setdefault('sent_at', timestamp())

        if options.get('properties'):
            raise InvalidParametersError('properties are not supported in identify calls')

        return Command(method='post', endpoint='identify', data=self.build_context(options))
