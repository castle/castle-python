from castle.headers_formatter import HeadersFormatter
from castle.configuration import configuration

BLACKLISTED = ['Cookie', 'Authorization']


class ExtractorsHeaders(object):
    def __init__(self, environ):
        self.environ = environ
        self.formatter = HeadersFormatter

    def call(self):
        headers = dict()
        has_whitelist = len(configuration.whitelisted) > 0
        extended_blacklisted = configuration.blacklisted + BLACKLISTED

        for key, value in self.environ.items():
            name = self.formatter.call(key)
            if has_whitelist and name not in configuration.whitelisted:
                headers[name] = True
                continue
            if name in extended_blacklisted:
                headers[name] = True
                continue
            headers[name] = value

        return headers
