import requests


class Session(object):
    class __Session:
        def __init__(self):
            self.session = requests.Session()

        def get(self):
            return self.session
    instance = None

    def __new__(cls):
        if not Session.instance:
            Session.instance = Session.__Session()
        return Session.instance

    def get(self):
        return self.instance.get()
