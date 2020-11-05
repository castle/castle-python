from castle.core.send_request import CoreSendRequest
from castle.core.process_response import CoreProcessResponse
from castle.configuration import configuration
from castle.exceptions import ConfigurationError


class Api(object):
    def __init__(self):
        self.req = CoreSendRequest({'Content-Type': 'application/json'})

    def request(self, command):
        if not configuration.isValid():
            raise ConfigurationError
        return self.req.build_query(command.method, command.path, command.data)

    def call(self, command):
        return CoreProcessResponse(self.request(command)).call()
