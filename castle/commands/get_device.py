from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsGetDevice(object):

    @staticmethod
    def call(device_token):
        ValidatorsPresent.call({'device_token': device_token}, 'device_token')

        return Command(
            method='get',
            path="devices/{device_token}".format(device_token=device_token),
            data=None
        )
