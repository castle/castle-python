from castle.exceptions import ConfigurationError
from castle.headers_formatter import HeadersFormatter

BLACK_LIST = ['HTTP_COOKIE', 'HTTP_AUTHORIZATION']

WHITE_LIST = [
    "Accept",
    "Accept-Charset",
    "Accept-Datetime",
    "Accept-Encoding",
    "Accept-Language",
    "Cache-Control",
    "Connection",
    "Content-Length",
    "Content-Type",
    "Cookie",
    "Host",
    "Origin",
    "Pragma",
    "Referer",
    "User-Agent",
]

# 500 milliseconds
REQUEST_TIMEOUT = 500
FAILOVER_STRATEGIES = ['allow', 'deny', 'challenge', 'throw']


class Configuration(object):
    def __init__(self):
        self.api_secret = None
        self.host = 'api.castle.io'
        self.port = 443
        self.url_prefix = '/v1'
        self.white_list = []
        self.black_list = BLACK_LIST
        self.request_timeout = REQUEST_TIMEOUT
        self.failover_strategy = 'allow'

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
    def white_list(self):
        return self.__white_list

    @white_list.setter
    def white_list(self, value):
        if value:
            self.__white_list = [HeadersFormatter.call(v) for v in value]
        else:
            self.__white_list = []

    @property
    def black_list(self):
        return self.__black_list

    @black_list.setter
    def black_list(self, value):
        if value:
            self.__black_list = [HeadersFormatter.call(v) for v in value] + BLACK_LIST
        else:
            self.__black_list = BLACK_LIST

    @property
    def request_timeout(self):
        return self.__request_timeout

    @request_timeout.setter
    def request_timeout(self, value):
        self.__request_timeout = value

    @property
    def failover_strategy(self):
        return self.__failover_strategy

    @failover_strategy.setter
    def failover_strategy(self, value):
        if value in FAILOVER_STRATEGIES:
            self.__failover_strategy = value
        else:
            raise ConfigurationError


# pylint: disable=invalid-name
configuration = Configuration()
