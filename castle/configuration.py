from castle.headers_formatter import HeadersFormatter

WHITELISTED = [
    'User-Agent',
    'Accept-Language',
    'Accept-Encoding',
    'Accept-Charset',
    'Accept',
    'Accept-Datetime',
    'X-Forwarded-For',
    'Forwarded',
    'X-Forwarded',
    'X-Real-IP',
    'REMOTE_ADDR'
]

BLACKLISTED = ['HTTP_COOKIE']


class ConfigurationObject(object):
    def __init__(self):
        self.host = 'api.castle.io'
        self.port = 443
        self.url_prefix = '/v1'
        self.whitelisted = WHITELISTED
        self.blacklisted = BLACKLISTED

    @property
    def whitelisted(self):
        return self.__whitelisted

    @whitelisted.setter
    def whitelisted(self, value):
        if value:
            self.__whitelisted = [HeadersFormatter.call(v) for v in value]
        else:
            self.__whitelisted = []

    @property
    def blacklisted(self):
        return self.__blacklisted

    @blacklisted.setter
    def blacklisted(self, value):
        if value:
            self.__blacklisted = [HeadersFormatter.call(v) for v in value]
        else:
            self.__blacklisted = []


configuration = ConfigurationObject()


def Configuration():
    """Simulate a singelton Configuration object for backward compatibility."""
    return configuration
