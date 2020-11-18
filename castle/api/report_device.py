from castle.api_request import APIRequest
from castle.commands.report_device import CommandsReportDevice


class APIReportDevice(object):
    @staticmethod
    def retrieve(device_token):
        return APIRequest().call(CommandsReportDevice.build(device_token))
