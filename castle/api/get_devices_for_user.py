from castle.api_request import APIRequest
from castle.commands.get_devices_for_user import CommandsGetDevicesForUser
from castle.configuration import configuration


class APIGetDevicesForUser(object):
    @staticmethod
    def call(user_id, config=configuration):
        return APIRequest(config).call(CommandsGetDevicesForUser.call(user_id))
