import re


class HeadersFormatter(object):
    @staticmethod
    def call(header):
        return HeadersFormatter.format(re.sub(r'^HTTP(?:_|-)', '', header, flags=re.I))

    @staticmethod
    def format(header):
        return '-'.join([v.capitalize() for v in re.split(r'_|-', header)])
