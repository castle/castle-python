import re

class HeadersFormatter(object):
    @staticmethod
    def call(header):
        return '-'.join([v.capitalize() for v in re.split(r'_|-', re.sub(r'^HTTP(?:_|-)', '', header, flags=re.IGNORECASE))])
