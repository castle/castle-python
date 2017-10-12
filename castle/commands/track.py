from castle.command import Command
from castle.commands.with_context import validate, WithContext


class CommandsTrack(WithContext):
    def build(self, options):
        validate(options, 'event')

        return Command(method='post', endpoint='track', data=self.build_context(options))
