from collections import namedtuple

from castle.test import unittest
from castle.headers.filter import HeadersFilter


def headers():
    return {
        'Action-Dispatch.request.content-Type': 'application/json',
        'HTTP_AUTHORIZATION': 'Basic 123456',
        'HTTP_COOKIE': "__cid=abcd;other=efgh",
        'HTTP_OK': 'OK',
        'HTTP_ACCEPT': 'application/json',
        'HTTP_X_FORWARDED_FOR': '1.2.3.4',
        'HTTP_USER_AGENT': 'Mozilla 1234',
        'TEST': '1',
        'REMOTE_ADDR': '1.2.3.4',
        'CONTENT_LENGTH': '0'
    }


def request():
    req = namedtuple('Request', ['ip', 'environ', 'COOKIES'])
    req.ip = '217.144.192.112'
    req.environ = headers()
    req.COOKIES = {}
    return req


class ExtractorsHeadersTestCase(unittest.TestCase):
    def test_filter_headers(self):
        self.assertEqual(HeadersFilter(request()).call(),
                         {
            'Accept': 'application/json',
            'Authorization': 'Basic 123456',
            'Cookie': "__cid=abcd;other=efgh",
            'Content-Length': '0',
            'Ok': 'OK',
            'User-Agent': 'Mozilla 1234',
            'Remote-Addr': '1.2.3.4',
            'X-Forwarded-For': '1.2.3.4'
        })
