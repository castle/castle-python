from castle.command import Command
from castle.commands.with_context import validate, WithContext


class CommandsAuthenticate(WithContext):
    def build(self, options):
        validate(options, 'event', 'user_id')

        return Command(method='post', endpoint='authenticate', data=self.build_context(options))
