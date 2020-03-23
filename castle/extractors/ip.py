import re
from castle.configuration import configuration, TRUSTED_PROXIES


# ordered list of ip headers for ip extraction
DEFAULT = ['X-Forwarded-For', 'Client-Ip', 'Remote-Addr']
# default header fallback when ip is not found
FALLBACK = 'Remote-Addr'

class ExtractorsIp(object):
    def __init__(self, headers):
        self.headers = headers
        self.ip_headers = configuration.ip_headers + DEFAULT
        self.proxies = configuration.trusted_proxies + TRUSTED_PROXIES

    def call(self):
        for ip_header in self.ip_headers:
            ip_value = self._calculate_ip(ip_header)
            if ip_value:
                return ip_value

        return self.headers.get(FALLBACK, None)

    def _calculate_ip(self, header):
        ips = self._ips_from(header)
        filtered_ips = self._remove_proxies(ips)

        if len(filtered_ips) > 0:
            return filtered_ips[0]
        return None

    def _remove_proxies(self, ips):
        result = []

        for ip_address in ips:
            if not self._is_proxy(ip_address):
                result.append(ip_address)
        return result

    def _is_proxy(self, ip_address):
        for proxy_re in self.proxies:
            if re.match(proxy_re, ip_address, flags=re.I|re.X):
                return True

        return False


    def _ips_from(self, header):
        value = self.headers.get(header)

        if not value:
            return []

        return re.split(r'[,\s]+', value.strip())[::-1]
