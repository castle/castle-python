import re
from castle.headers.format import HeadersFormat

VALUABLE_HEADERS = r"""^
      HTTP(?:_|-).*|
      CONTENT(?:_|-)LENGTH|
      REMOTE(?:_|-)ADDR
$"""


class HeadersFilter(object):
    def __init__(self, request):
        self.environ = request.environ
        self.formatter = HeadersFormat

    def call(self):
        result = dict()

        for header_name, value in self.environ.items():
            if not re.match(VALUABLE_HEADERS, header_name, flags=re.X | re.I):
                continue

            formatted_name = HeadersFormat.call(header_name)
            result[formatted_name] = value

        return result
