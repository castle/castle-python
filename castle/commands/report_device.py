from castle.command import Command


class CommandsReportDevice(object):

    @staticmethod
    def call(device_token):
        return Command(
            method='put',
            path="devices/{device_token}/report".format(device_token=device_token),
            data=None
        )
