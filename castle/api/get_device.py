from castle.api_request import APIRequest
from castle.commands.get_devices import CommandsGetDevice


class APIGetDevice(object):
    @staticmethod
    def retrieve(device_token):
        return APIRequest().call(CommandsGetDevice.build(device_token))
