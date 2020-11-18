from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsApproveDevice(object):

    @staticmethod
    def build(device_token):
        ValidatorsPresent.call({'device_token': device_token}, 'device_token')

        return Command(
            method='put',
            path="devices/{device_token}/approve".format(device_token=device_token),
            data=None
        )
