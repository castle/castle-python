from castle.command import Command


class CommandsEventsSchema(object):
    @staticmethod
    def call(options=None):
        return Command(method='get', path='events/schema', data=None)
