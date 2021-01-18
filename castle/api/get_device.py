from castle.api_request import APIRequest
from castle.commands.get_device import CommandsGetDevice
from castle.configuration import configuration

class APIGetDevice(object):
    @staticmethod
    def call(device_token, config = configuration):
        return APIRequest(config).call(CommandsGetDevice.call(device_token))
