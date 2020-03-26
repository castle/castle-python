from castle.configuration import configuration

ALWAYS_BLACKLISTED = ['Cookie', 'Authorization']
ALWAYS_WHITELISTED = ['User-Agent']


class ExtractorsHeaders(object):
    def __init__(self, headers):
        self.headers = headers
        self.no_whitelist = len(configuration.whitelisted) == 0

    def call(self):
        result = dict()

        for name, value in self.headers.items():
            result[name] = self._header_value(name, value)

        return result

    def _header_value(self, name, value):
        if name in ALWAYS_BLACKLISTED:
            return True
        if name in ALWAYS_WHITELISTED:
            return value
        if name in configuration.blacklisted:
            return True
        if self.no_whitelist or (name in configuration.whitelisted):
            return value

        return True
