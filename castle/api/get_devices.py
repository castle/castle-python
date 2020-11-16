from castle.api_request import APIRequest
from castle.commands.get_devices import CommandsGetDevices


class APIGetDevices(object):
    @staticmethod
    def retrieve(user_id):
        return APIRequest().call(CommandsGetDevices.build(user_id))
