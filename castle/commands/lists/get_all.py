from castle.command import Command


class CommandsListsGetAll(object):
    @staticmethod
    def call(options=None):
        return Command(method='get', path='lists', data=None)
