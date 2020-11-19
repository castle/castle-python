from castle.api_request import APIRequest
from castle.commands.get_devices_for_user import CommandsGetDevicesForUser


class APIGetDevicesForUser(object):
    @staticmethod
    def retrieve(user_id):
        return APIRequest().call(CommandsGetDevicesForUser.build(user_id))
