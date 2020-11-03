import json
from castle.configuration import configuration
from castle.apis.session import ApisSession

HTTPS_SCHEME = 'https'

class ApisRequest(object):
    def __init__(self, headers=None):
        self.headers = headers or dict()
        self.base_url = ApisRequest.build_base_url()
        self.session = ApisSession()

    def build_query(self, method, path, params):
        return self.session.get().request(
            method,
            self.build_url(path),
            auth=('', configuration.api_secret),
            timeout=configuration.request_timeout / 1000.0,
            headers=self.headers,
            verify=ApisRequest.verify(),
            data=None if params is None else json.dumps(params)
        )

    def build_url(self, path):
        return '{base}/{action}'.format(base=self.base_url, action=path)

    @staticmethod
    def build_base_url():
        template = 'http://{host}:{port}/{prefix}'

        if configuration.base_url.scheme == HTTPS_SCHEME:
            template = 'https://{host}/{prefix}'

        return template.format(
            host=configuration.base_url.hostname,
            port=configuration.base_url.port,
            prefix=configuration.base_url.path
        )

    @staticmethod
    def verify():
        return configuration.base_url.port == 443
