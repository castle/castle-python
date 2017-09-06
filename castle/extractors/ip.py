class ExtractorsIp(object):
    def __init__(self, request):
        self.request = request

    def call(self):
        if hasattr(self.request, 'ip'):
            return self.request.ip
        else:
            return self.wsgi_request_ip()

    def wsgi_request_ip(self):
        x_forwarded_for = self.request.environ.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.environ.get('REMOTE_ADDR')

        return ip
