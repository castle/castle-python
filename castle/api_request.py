from castle.core.send_request import CoreSendRequest
from castle.core.process_response import CoreProcessResponse
from castle.configuration import configuration
from castle.errors import ConfigurationError


class APIRequest(object):
    def __init__(self, config=configuration):
        self.req = CoreSendRequest({'Content-Type': 'application/json'})
        self.config = config

    def request(self, command):
        if not self.config.isValid():
            raise ConfigurationError
        return self.req.build_query(command.method, command.path, command.data, self.config)

    def call(self, command):
        return CoreProcessResponse(self.request(command)).call()
