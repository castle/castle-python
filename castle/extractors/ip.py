class ExtractorsIp(object):
    def __init__(self, request):
        self.request = request

    def call(self):
        return self.request.ip()
