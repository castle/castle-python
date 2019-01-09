import requests


class SessionSharer(object):
    class __SessionSharer:
        def __init__(self):
            self.session = requests.Session()
    instance = None

    def __new__(cls):
        if not SessionSharer.instance:
            SessionSharer.instance = SessionSharer.__SessionSharer()
        return SessionSharer.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
