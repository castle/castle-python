from castle.version import VERSION
from castle.extractors.client_id import ExtractorsClientId
from castle.extractors.headers import ExtractorsHeaders
from castle.extractors.ip import ExtractorsIp

__version__ = VERSION


class ContextDefault(object):
    def __init__(self, request, cookies):
        used_cookies = self._fetch_cookies(request, cookies)
        self.client_id = ExtractorsClientId(
            request.environ, used_cookies).call()
        self.headers = ExtractorsHeaders(request.environ).call()
        self.request_ip = ExtractorsIp(request).call()

    def _defaults(self):
        return {
            'client_id': self.client_id,
            'active': True,
            'origin': 'web',
            'headers': self.headers,
            'ip': self.request_ip,
            'library': {'name': 'castle-python', 'version': __version__}
        }

    def _defaults_extra(self):
        context = dict()
        if 'Accept-Language' in self.headers:
            context['locale'] = self.headers['Accept-Language']
        if 'User-Agent' in self.headers:
            context['user_agent'] = self.headers['User-Agent']
        return context

    def call(self):
        context = dict(self._defaults())
        context.update(self._defaults_extra())
        return context

    @staticmethod
    def _fetch_cookies(request, cookies):
        if cookies:
            return cookies
        elif hasattr(request, 'COOKIES') and request.COOKIES:
            return request.COOKIES
        return None
