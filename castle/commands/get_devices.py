from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsGetDevices(object):

    @staticmethod
    def build(user_id):
        ValidatorsPresent.call({'user_id': user_id}, 'user_id')

        return Command(
            method='get',
            path="{user_id}/devices".format(user_id=user_id),
            data=None
        )
