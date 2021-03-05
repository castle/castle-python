class FingerprintExtract(object):
    def __init__(self, headers, cookies=None):
        self.headers = headers
        self.cookies = cookies or dict()

    def call(self):
        return self.headers.get('X-Castle-Client-Id', self.cookies.get('__cid', ''))
