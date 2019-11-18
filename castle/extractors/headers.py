from castle.headers_formatter import HeadersFormatter
from castle.configuration import configuration, BLACK_LIST


class ExtractorsHeaders(object):
    def __init__(self, environ):
        self.environ = environ
        self.formatter = HeadersFormatter

    def call(self):
        headers = dict()
        has_whitelist = len(configuration.white_list) > 0
        extended_black_list = configuration.black_list + BLACK_LIST

        for key, value in self.environ.items():
            name = self.formatter.call(key)
            if has_whitelist and name not in configuration.white_list:
                headers[name] = True
                continue
            if name in extended_black_list:
                headers[name] = True
                continue
            headers[name] = value

        return headers
