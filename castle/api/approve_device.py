from castle.api_request import APIRequest
from castle.commands.approve_device import CommandsApproveDevice


class APIApproveDevice(object):
    @staticmethod
    def call(device_token):
        return APIRequest().call(CommandsApproveDevice.build(device_token))
