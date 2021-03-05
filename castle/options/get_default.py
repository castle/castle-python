from castle.version import VERSION
from castle.headers.filter import HeadersFilter
from castle.fingerprint.extract import FingerprintExtract
from castle.headers.extract import HeadersExtract
from castle.ips.extract import IPsExtract

__version__ = VERSION


class OptionsGetDefault(object):
    def __init__(self, request, cookies):
        self.cookies = self._fetch_cookies(request, cookies)
        self.pre_headers = HeadersFilter(request).call()

    def call(self):
        context = dict({
            'fingerprint': self._fingerprint(),
            'active': True,
            'headers': self._headers(),
            'ip': self._ip(),
            'library': {
                'name': 'castle-python',
                'version': __version__
            }
        })
        context.update(self._optional_defaults())

        return context

    def _ip(self):
        return IPsExtract(self.pre_headers).call()

    def _fingerprint(self):
        return FingerprintExtract(self.pre_headers, self.cookies).call()

    def _headers(self):
        return HeadersExtract(self.pre_headers).call()

    def _optional_defaults(self):
        context = dict()
        if 'Accept-Language' in self.pre_headers:
            context['locale'] = self.pre_headers.get('Accept-Language')
        if 'User-Agent' in self.pre_headers:
            context['user_agent'] = self.pre_headers.get('User-Agent')
        return context

    @staticmethod
    def _fetch_cookies(request, cookies):
        if cookies:
            return cookies
        if hasattr(request, 'COOKIES') and request.COOKIES:
            return request.COOKIES
        return None
