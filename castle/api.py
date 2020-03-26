from castle.apis.request import ApisRequest
from castle.apis.response import ApisResponse
from castle.configuration import configuration
from castle.exceptions import ConfigurationError


class Api(object):
    def __init__(self):
        self.req = ApisRequest({'Content-Type': 'application/json'})

    def request(self, command):
        if not configuration.isValid():
            raise ConfigurationError
        return self.req.build_query(command.method, command.path, command.data)

    def call(self, command):
        return ApisResponse(self.request(command)).call()
