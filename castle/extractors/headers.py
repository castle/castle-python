from castle.headers_formatter import HeadersFormatter
from castle.configuration import configuration

DEFAULT_BLACKLIST = ['Cookie', 'Authorization']
DEFAULT_WHITELIST = ['User-Agent']


class ExtractorsHeaders(object):
    def __init__(self, environ):
        self.environ = environ
        self.formatter = HeadersFormatter

    def call(self):
        headers = dict()
        has_whitelist = len(configuration.whitelisted) > 0

        for key, value in self.environ.items():
            name = self.formatter.call(key)
            if has_whitelist and name not in configuration.whitelisted and name not in DEFAULT_WHITELIST:
                headers[name] = True
                continue
            if name in configuration.blacklisted or name in DEFAULT_BLACKLIST:
                headers[name] = True
                continue
            headers[name] = value

        return headers
