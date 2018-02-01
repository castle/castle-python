from castle.command import Command
from castle.commands.with_context import validate, WithContext
from castle.utils import timestamp


class CommandsAuthenticate(WithContext):
    def build(self, options):
        validate(options, 'event', 'user_id')
        options.setdefault('sent_at', timestamp())

        return Command(method='post', endpoint='authenticate', data=self.build_context(options))
