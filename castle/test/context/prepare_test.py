from collections import namedtuple
from castle.context.prepare import ContextPrepare
from castle.test import unittest
from castle.version import VERSION


def request():
    req = namedtuple('Request', ['ip', 'environ', 'COOKIES'])
    req.ip = '217.144.192.112'
    req.environ = {'HTTP_X_FORWARDED_FOR': '217.144.192.112',
                   'HTTP-User-Agent': 'test',
                   'HTTP_X_CASTLE_CLIENT_ID': '1234'}
    req.COOKIES = {}
    return req


class ContextPrepareTestCase(unittest.TestCase):

    def test_call(self):
        context = {
            'active': True,
            'fingerprint': '1234',
            'headers': {
                'User-Agent': 'test',
                'X-Forwarded-For': '217.144.192.112',
                'X-Castle-Client-Id': '1234'
            },
            'ip': '217.144.192.112',
            'library': {'name': 'castle-python', 'version': VERSION}
        }
        result_context = ContextPrepare.call(request(), {})
        self.assertEqual(result_context, context)

    def test_setup_fingerprint_from_cookies(self):
        cookies = {'__cid': '1234'}
        options = {'cookies': cookies}
        result_context = ContextPrepare.call(request(), options)
        self.assertEqual(result_context['fingerprint'], '1234')
