class ExtractorsClientId(object):
    def __init__(self, environ, cookies=dict()):
        self.environ = environ
        self.cookies = cookies

    def call(self):
        return self.cookies.get('__cid', self.environ.get('HTTP_X_CASTLE_CLIENT_ID', ''))
