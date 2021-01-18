from castle.configuration import configuration

ALWAYS_DENYLISTED = ['Cookie', 'Authorization']
ALWAYS_ALLOWLISTED = ['User-Agent']


class HeadersExtract(object):
    def __init__(self, headers, config = configuration):
        self.headers = headers
        self.no_whitelist = len(config.allowlisted) == 0

    def call(self):
        result = dict()

        for name, value in self.headers.items():
            result[name] = self._header_value(name, value)

        return result

    def _header_value(self, name, value, config = configuration):
        if name in ALWAYS_DENYLISTED:
            return True
        if name in ALWAYS_ALLOWLISTED:
            return value
        if name in config.denylisted:
            return True
        if self.no_whitelist or (name in config.allowlisted):
            return value

        return True
