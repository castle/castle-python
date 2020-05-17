from castle.exceptions import ConfigurationError
from castle.headers_formatter import HeadersFormatter

DEFAULT_WHITELIST = [
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
    "TE",
    "Upgrade-Insecure-Requests",
    "User-Agent",
    "X-Castle-Client-Id",
]

# 500 milliseconds
REQUEST_TIMEOUT = 500
FAILOVER_STRATEGIES = ['allow', 'deny', 'challenge', 'throw']
HOST = 'api.castle.io'
PORT = 443
URL_PREFIX = '/v1'
FAILOVER_STRATEGY = 'allow'
TRUSTED_PROXIES = [r"""
        \A127\.0\.0\.1\Z|
        \A(10|172\.(1[6-9]|2[0-9]|30|31)|192\.168)\.|
        \A::1\Z|\Afd[0-9a-f]{2}:.+|
        \Alocalhost\Z|
        \Aunix\Z|
        \Aunix:"""]


class Configuration(object):
    def __init__(self):
        self.api_secret = None
        self.host = HOST
        self.port = PORT
        self.url_prefix = URL_PREFIX
        self.whitelisted = []
        self.blacklisted = []
        self.request_timeout = REQUEST_TIMEOUT
        self.failover_strategy = FAILOVER_STRATEGY
        self.ip_headers = []
        self.trusted_proxies = []
        self.trust_proxy_chain = False
        self.trusted_proxy_depth = None

    def isValid(self):
        return self.host and self.port and self.api_secret

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

    @property
    def failover_strategy(self):
        return self.__failover_strategy

    @failover_strategy.setter
    def failover_strategy(self, value):
        if value in FAILOVER_STRATEGIES:
            self.__failover_strategy = value
        else:
            raise ConfigurationError

    @property
    def ip_headers(self):
        return self.__ip_headers

    @ip_headers.setter
    def ip_headers(self, value):
        if isinstance(value, list):
            self.__ip_headers = [HeadersFormatter.call(v) for v in value]
        else:
            raise ConfigurationError

    @property
    def trusted_proxies(self):
        return self.__trusted_proxies

    @trusted_proxies.setter
    def trusted_proxies(self, value):
        if isinstance(value, list):
            self.__trusted_proxies = value
        else:
            raise ConfigurationError

    @property
    def trust_proxy_chain(self):
        return self.__trust_proxy_chain

    @trust_proxy_chain.setter
    def trust_proxy_chain(self, value):
        if isinstance(value, bool):
            self.__trust_proxy_chain = value
        else:
            raise ConfigurationError

    @property
    def trusted_proxies_depth(self):
        return self.__trusted_proxies_depth

    @trusted_proxies_depth.setter
    def trusted_proxies_depth(self, value):
        if isinstance(value, (int, type(None))):
            self.__trusted_proxies_depth = int(0 if value is None else value)
        else:
            raise ConfigurationError

# pylint: disable=invalid-name
configuration = Configuration()
