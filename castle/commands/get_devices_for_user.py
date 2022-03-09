from castle.command import Command


class CommandsGetDevicesForUser(object):

    @staticmethod
    def call(user_id):
        return Command(
            method='get',
            path="users/{user_id}/devices".format(user_id=user_id),
            data=None
        )
