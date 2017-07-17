import json
import requests
import pdb
from castle.configuration import configuration


class Request(object):
    def __init__(self, headers=None):
        self.headers = headers or dict()
        self.base_url = self.build_base_url()

    def build_query(self, method, endpoint, params):
        return requests.request(
            method,
            self.build_url(endpoint),
            auth=('', configuration.api_secret),
            # timeout=configuration.request_timeout,
            headers=self.headers,
            verify=self.verify(),
            data=json.dumps(params)
        )

    def build_url(self, endpoint):
        return '{base}/{action}'.format(base=self.base_url, action=endpoint.split('/')[-1])

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
