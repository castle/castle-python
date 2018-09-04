import re
import sys


class HeadersFormatter(object):
    @staticmethod
    def call(header):
        return '-'.join([v.capitalize() for v in HeadersFormatter.split(header)])

    @staticmethod
    def split(header):
        if sys.version_info[:2] == (2, 6):
            return re.split(r'_|-', re.sub(re.compile(r'^HTTP(?:_|-)', re.IGNORECASE), '', header))
        else:
            return re.split(r'_|-', re.sub(r'^HTTP(?:_|-)', '', header, flags=re.IGNORECASE))
