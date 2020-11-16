from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsGetDevices(object):

    @staticmethod
    def build(device_token):
        ValidatorsPresent.call({'device_token': device_token}, 'device_token')

        return Command(
            method='get',
            path="devices/{device_token}".format(device_token=device_token),
            data=None
        )
