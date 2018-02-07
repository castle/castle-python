from castle.command import Command
from castle.commands.with_context import validate, WithContext
from castle.utils import timestamp


class CommandsTrack(WithContext):
    def build(self, options):
        validate(options, 'event')
        options.setdefault('sent_at', timestamp())

        return Command(method='post', path='track', data=self.build_context(options))
