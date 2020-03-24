import requests


class ApisSessionSharer(object):
    class __ApisSessionSharer:
        def __init__(self):
            self.session = requests.Session()
    instance = None

    def __new__(cls):
        if not ApisSessionSharer.instance:
            ApisSessionSharer.instance = ApisSessionSharer.__ApisSessionSharer()
        return ApisSessionSharer.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
