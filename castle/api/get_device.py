from castle.api_request import APIRequest
from castle.commands.get_device import CommandsGetDevice


class APIGetDevice(object):
    @staticmethod
    def call(device_token):
        return APIRequest().call(CommandsGetDevice.call(device_token))
