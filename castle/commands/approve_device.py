from castle.command import Command


class CommandsApproveDevice(object):

    @staticmethod
    def call(device_token):
        return Command(
            method='put',
            path="devices/{device_token}/approve".format(device_token=device_token),
            data=None
        )
