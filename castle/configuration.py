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

# 500 milliseconds
REQUEST_TIMEOUT = 0.5


class ConfigurationObject(object):
    def __init__(self):
        self.api_secret = None
        self.host = 'api.castle.io'
        self.port = 443
        self.url_prefix = '/v1'
        self.whitelisted = WHITELISTED
        self.blacklisted = BLACKLISTED
        self.request_timeout = REQUEST_TIMEOUT

    @property
    def api_secret(self):
        return self.__api_secret

    @api_secret.setter
    def api_secret(self, value):
        self.__api_secret = value

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def url_prefix(self):
        return self.__url_prefix

    @url_prefix.setter
    def url_prefix(self, value):
        self.__url_prefix = value

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

    @property
    def request_timeout(self):
        return self.__request_timeout

    @request_timeout.setter
    def request_timeout(self, value):
        self.__request_timeout = value


configuration = ConfigurationObject()


def Configuration():
    """Simulate a singelton Configuration object for backward compatibility."""
    return configuration
