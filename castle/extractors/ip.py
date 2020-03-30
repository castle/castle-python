import re
from castle.configuration import configuration, TRUSTED_PROXIES


# ordered list of ip headers for ip extraction
DEFAULT = ['X-Forwarded-For', 'Remote-Addr']


class ExtractorsIp(object):
    def __init__(self, headers):
        self.headers = headers
        if len(configuration.ip_headers) > 0:
            self.ip_headers = configuration.ip_headers
        else:
            self.ip_headers = DEFAULT
        self.proxies = configuration.trusted_proxies + TRUSTED_PROXIES

    def call(self):
        all_ips = []

        for ip_header in self.ip_headers:
            ips = self._ips_from(ip_header)
            filtered_ips = self._remove_proxies(ips)

            if len(filtered_ips) > 0:
                return filtered_ips[-1]

            all_ips = all_ips + ips

        # fallback to first whatever ip
        if len(all_ips) > 0:
            return all_ips[0]

        return None

    def _remove_proxies(self, ips):
        result = []

        for ip_address in ips:
            if not self._is_proxy(ip_address):
                result.append(ip_address)
        return result

    def _is_proxy(self, ip_address):
        for proxy_re in self.proxies:
            if re.match(proxy_re, ip_address, flags=re.I | re.X):
                return True

        return False

    def _ips_from(self, header):
        value = self.headers.get(header)

        if not value:
            return []

        return re.split(r'[,\s]+', value.strip())
