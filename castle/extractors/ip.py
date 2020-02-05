class ExtractorsIp(object):
    def __init__(self, request):
        self.request = request

    def call(self):
        if hasattr(self.request, 'ip'):
            return self.request.ip

        return self.request.environ.get('REMOTE_ADDR')
