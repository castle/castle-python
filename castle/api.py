from castle.request import Request
from castle.response import Response


class Api(object):
    def __init__(self):
        self.req = Request({'Content-Type': 'application/json'})

    def request(self, command):
        return self.req.build_query(command.method, command.path, command.data)

    def call(self, command):
        return Response(self.request(command)).call()
