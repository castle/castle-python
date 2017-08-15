import requests
from castle.configuration import configuration


class Request(object):
    def __init__(self, headers=None):
        self.headers = headers or dict()
        self.base_url = self.build_base_url()

    def build_query(self, method, endpoint, params):
        return requests.request(
            method,
            self.build_url(endpoint),
            self.build_query_params(params)
        )

    def build_query_params(self, params):
        return dict(
            headers=self.headers,
            timeout=configuration.request_timeout,
            auth=('', configuration.api_secret),
            verify=self.verify(),
            params=params
        )

    def build_url(self, endpoint):
        return '{base}/{action}'.format(base=self.base_url, action=endpoint.split('/'))

    def build_base_url(self):
        template = 'http://{host}:{port}/{prefix}'

        if configuration.port == 443:
            template = 'https://{host}/{prefix}'

        return template.format(
            host=configuration.host.strip('/'),
            port=configuration.port,
            prefix=configuration.url_prefix.strip('/')
        )

    def verify(self):
        return True if configuration.port == 443 else False
