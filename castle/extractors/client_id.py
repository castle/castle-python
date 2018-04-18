class ExtractorsClientId(object):
    def __init__(self, environ, cookies=None):
        self.environ = environ
        self.cookies = cookies or dict()

    def call(self):
        return self.environ.get('HTTP_X_CASTLE_CLIENT_ID', self.cookies.get('__cid', ''))
