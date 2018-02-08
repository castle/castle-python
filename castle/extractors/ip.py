class ExtractorsIp(object):
    def __init__(self, request):
        self.request = request

    def call(self):
        if hasattr(self.request, 'ip'):
            return self.request.ip

        return self.wsgi_request_ip()

    def wsgi_request_ip(self):
        cf_ip = self.request.environ.get('HTTP_CF_CONNECTING_IP')

        if cf_ip:
            return cf_ip.split(',')[0]

        x_forwarded_for = self.request.environ.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return self.request.environ.get('REMOTE_ADDR')
