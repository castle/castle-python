import json
from castle.configuration import configuration
from castle.logger import Logger
from castle.session import Session

HTTPS_SCHEME = 'https'


class CoreSendRequest(object):
    def __init__(self, headers=None):
        self.headers = headers or dict()
        self.base_url = CoreSendRequest.build_base_url()
        self.session = Session()

    def build_query(self, method, path, params, config=configuration):
        url = self.build_url(path)
        request_data = {
            "auth": ('', config.api_secret),
            "timeout": config.request_timeout / 1000.0,
            "headers": self.headers,
            "verify": CoreSendRequest.verify(),
            "data": None if params is None else json.dumps(params)
        }

        Logger.call("{}:".format(url), request_data.get("data"))

        return self.session.get().request(
            method,
            url,
            **request_data
        )

    def build_url(self, path):
        return '{base}/{action}'.format(base=self.base_url, action=path)

    @staticmethod
    def build_base_url():
        return configuration.base_url.geturl()

    @staticmethod
    def verify():
        return configuration.base_url.scheme == HTTPS_SCHEME
