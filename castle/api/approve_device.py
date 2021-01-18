from castle.api_request import APIRequest
from castle.commands.approve_device import CommandsApproveDevice
from castle.configuration import configuration


class APIApproveDevice(object):
    @staticmethod
    def call(device_token, config=configuration):
        return APIRequest(config).call(CommandsApproveDevice.call(device_token))
