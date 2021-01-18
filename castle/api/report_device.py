from castle.api_request import APIRequest
from castle.commands.report_device import CommandsReportDevice
from castle.configuration import configuration

class APIReportDevice(object):
    @staticmethod
    def call(device_token, config = configuration):
        return APIRequest(config).call(CommandsReportDevice.call(device_token))
