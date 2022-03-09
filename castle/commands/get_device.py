from castle.command import Command


class CommandsGetDevice(object):

    @staticmethod
    def call(device_token):
        return Command(
            method='get',
            path="devices/{device_token}".format(device_token=device_token),
            data=None
        )
