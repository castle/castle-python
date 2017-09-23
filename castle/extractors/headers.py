from castle.headers_formatter import HeadersFormatter
from castle.configuration import configuration


class ExtractorsHeaders(object):
    def __init__(self, environ):
        self.environ = environ
        self.formatter = HeadersFormatter

    def call(self):
        headers = dict()

        for key, value in self.environ.items():
            name = self.formatter.call(key)
            if name not in configuration.whitelisted:
                continue
            if name in configuration.blacklisted:
                continue
            headers[name] = value

        return headers
