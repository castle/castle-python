from castle.headers_formatter import HeadersFormatter
from castle.configuration import configuration


class ExtractorsHeaders(object):
    def __init__(self, environ):
        self.environ = environ
        self.formatter = HeadersFormatter

    def call(self):
        headers = dict()
        has_whitelist = len(configuration.white_list) > 0

        for key, value in self.environ.items():
            name = self.formatter.call(key)
            if has_whitelist and name not in configuration.white_list:
                continue
            if name in configuration.black_list:
                continue
            headers[name] = value

        return headers
