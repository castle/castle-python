from castle.configuration import configuration


class ExtractorsIp(object):
    def __init__(self, request):
        self.request = request

    def call(self):
        ip_address = self.get_ip_from_headers()
        if ip_address:
            return ip_address

        if hasattr(self.request, 'ip'):
            return self.request.ip

        return self.request.environ.get('REMOTE_ADDR')

    def get_ip_from_headers(self):
        for header in configuration.ip_headers:
            value = self.request.environ.get(header)
            if value:
                return value
        return None
