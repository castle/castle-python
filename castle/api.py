from castle.apis.request import ApisRequest
from castle.apis.response import ApisResponse


class Api(object):
    def __init__(self):
        self.req = ApisRequest({'Content-Type': 'application/json'})

    def request(self, command):
        return self.req.build_query(command.method, command.path, command.data)

    def call(self, command):
        return ApisResponse(self.request(command)).call()
