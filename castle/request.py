import json
import requests
from castle.configuration import configuration


class Request(object):
    def __init__(self, headers=None):
        self.headers = headers or dict()
        self.base_url = Request.build_base_url()

    def build_query(self, method, path, params):
        return requests.request(
            method,
            self.build_url(path),
            auth=('', configuration.api_secret),
            timeout=configuration.request_timeout / 1000.0,
            headers=self.headers,
            verify=Request.verify(),
            data=None if params is None else json.dumps(params)
        )

    def build_url(self, path):
        return '{base}/{action}'.format(base=self.base_url, action=path)

    @staticmethod
    def build_base_url():
        template = 'http://{host}:{port}/{prefix}'

        if configuration.port == 443:
            template = 'https://{host}/{prefix}'

        return template.format(
            host=configuration.host.strip('/'),
            port=configuration.port,
            prefix=configuration.url_prefix.strip('/')
        )

    @staticmethod
    def verify():
        return True if configuration.port == 443 else False
