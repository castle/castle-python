from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsReportDevice(object):

    @staticmethod
    def build(device_token):
        ValidatorsPresent.call({'device_token': device_token}, 'device_token')

        return Command(
            method='put',
            path="devices/{device_token}/report".format(device_token=device_token),
            data=None
        )
