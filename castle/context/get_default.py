from castle.version import VERSION
from castle.headers.filter import HeadersFilter
from castle.headers.extract import HeadersExtract
from castle.ips.extract import IPsExtract

__version__ = VERSION


class ContextGetDefault(object):
    def __init__(self, request):
        self.pre_headers = HeadersFilter(request).call()

    def call(self):
        return dict(
            {
                'headers': self._headers(),
                'ip': self._ip(),
                'library': {'name': 'castle-python', 'version': __version__},
            }
        )

    def _ip(self):
        return IPsExtract(self.pre_headers).call()

    def _headers(self):
        return HeadersExtract(self.pre_headers).call()
