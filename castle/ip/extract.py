import re
from castle.configuration import configuration, TRUSTED_PROXIES


# ordered list of ip headers for ip extraction
DEFAULT = ['X-Forwarded-For', 'Remote-Addr']
# list of header which are used with proxy depth setting
DEPTH_RELATED = ['X-Forwarded-For']


class IPExtract(object):
    def __init__(self, headers, config = configuration):
        self.headers = headers
        if len(config.ip_headers) > 0:
            self.ip_headers = config.ip_headers
        else:
            self.ip_headers = DEFAULT
        self.proxies = config.trusted_proxies + TRUSTED_PROXIES
        self.trust_proxy_chain = config.trust_proxy_chain
        self.trusted_proxy_depth = config.trusted_proxy_depth

    def call(self):
        all_ips = []

        for ip_header in self.ip_headers:
            ips = self._ips_from(ip_header)
            ip_value = self._remove_proxies(ips)
            if ip_value:
                return ip_value
            all_ips += ips

        return next(iter(all_ips), None)

    def _remove_proxies(self, ips):
        if self.trust_proxy_chain:
            return next(iter(ips), None)

        result = [ip_address for ip_address in ips if not self._is_proxy(ip_address)]
        return (result or [None])[-1]

    def _is_proxy(self, ip_address):
        for proxy_re in self.proxies:
            if re.match(proxy_re, ip_address, flags=re.I | re.X):
                return True

        return False

    def _ips_from(self, header):
        value = self.headers.get(header)

        if not value:
            return []

        ips = re.split(r'[,\s]+', value.strip())

        return self._limit_proxy_depth(ips, header)

    def _limit_proxy_depth(self, ips, ip_header):
        if ip_header in DEPTH_RELATED:
            ips = ips[:len(ips)-self.trusted_proxy_depth]

        return ips
