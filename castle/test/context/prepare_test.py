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
            'library': {'name': 'castle-python', 'version': VERSION}
        }
        result_context = ContextPrepare.call({})
        self.assertEqual(result_context, context)
