from urllib.parse import urlparse, ParseResult
from castle.exceptions import ConfigurationError
from castle.headers.format import HeadersFormat

DEFAULT_ALLOWLIST = [
    "Accept",
    "Accept-Charset",
    "Accept-Datetime",
    "Accept-Encoding",
    "Accept-Language",
    "Cache-Control",
    "Connection",
    "Content-Length",
    "Content-Type",
    "Dnt",
    "Host",
    "Origin",
    "Pragma",
    "Referer",
    "Sec-Fetch-Dest",
    "Sec-Fetch-Mode",
    "Sec-Fetch-Site",
    "Sec-Fetch-User",
    "TE",
    "Upgrade-Insecure-Requests",
    "User-Agent",
    "X-Castle-Client-Id",
]

# API endpoint
BASE_URL = 'https://api.castle.io/v1'
FAILOVER_STRATEGY = 'allow'
# 500 milliseconds
REQUEST_TIMEOUT = 500
# regexp of trusted proxies which is always appended to the trusted proxy list
FAILOVER_STRATEGIES = ['allow', 'deny', 'challenge', 'throw']
TRUSTED_PROXIES = [r"""
        \A127\.0\.0\.1\Z|
        \A(10|172\.(1[6-9]|2[0-9]|30|31)|192\.168)\.|
        \A::1\Z|\Afd[0-9a-f]{2}:.+|
        \Alocalhost\Z|
        \Aunix\Z|
        \Aunix:"""]


class Configuration(object):
    def __init__(self):
        self.request_timeout = REQUEST_TIMEOUT
        self.failover_strategy = FAILOVER_STRATEGY
        self.base_url = urlparse(BASE_URL)
        self.allowlisted = []
        self.denylisted = []
        self.api_secret = None
        self.ip_headers = []
        self.trusted_proxies = []
        self.trust_proxy_chain = False
        self.trusted_proxy_depth = None

    def isValid(self):
        return self.api_secret and self.base_url.hostname

    @property
    def api_secret(self):
        return self.__api_secret

    @api_secret.setter
    def api_secret(self, value):
        self.__api_secret = value

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, value):
        if isinstance(value, ParseResult):
            self.__base_url = value
        else:
            self.__base_url = urlparse(value)

    @property
    def allowlisted(self):
        return self.__allowlisted

    @allowlisted.setter
    def allowlisted(self, value):
        if value:
            self.__allowlisted = [HeadersFormat.call(v) for v in value]
        else:
            self.__allowlisted = []

    @property
    def denylisted(self):
        return self.__denylisted

    @denylisted.setter
    def denylisted(self, value):
        if value:
            self.__denylisted = [HeadersFormat.call(v) for v in value]
        else:
            self.__denylisted = []

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
            self.__ip_headers = [HeadersFormat.call(v) for v in value]
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
    def trusted_proxy_depth(self):
        return self.__trusted_proxy_depth

    @trusted_proxy_depth.setter
    def trusted_proxy_depth(self, value):
        if isinstance(value, (int, type(None))):
            self.__trusted_proxy_depth = int(0 if value is None else value)
        else:
            raise ConfigurationError


# pylint: disable=invalid-name
configuration = Configuration()
