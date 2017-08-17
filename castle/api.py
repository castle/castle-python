from castle.request import Request
from castle.response import Response


class Api(object):
    def __init__(self):
        # TODO: remove those headers
        self.req = Request({'X-Castle-Ip': '217.144.192.112', 'X-Castle-Client-Id': '1234', 'X-Castle-User-Agent': 'castle-python/1.0'})

    def request(self, command):
        return self.req.build_query(command.method, command.endpoint, command.data)

    def response(self, req):
        return Response(req).call()

    def call(self, command):
        return self.response(self.request(command))
