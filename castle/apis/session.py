import requests


class ApisSession(object):
    class __ApisSession:
        def __init__(self):
            self.session = requests.Session()

        def get(self):
            return self.session
    instance = None

    def __new__(cls):
        if not ApisSession.instance:
            ApisSession.instance = ApisSession.__ApisSession()
        return ApisSession.instance

    def get(self):
        return self.instance.get()
