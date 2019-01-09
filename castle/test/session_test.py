from collections import namedtuple
from castle.test import unittest
from castle.client import Client


def request():
    req = namedtuple('Request', ['ip', 'environ', 'COOKIES'])
    req.ip = '217.144.192.112'
    req.environ = {'HTTP_X_FORWARDED_FOR': '217.144.192.112',
                   'HTTP-User-Agent': 'test',
                   'HTTP_X_CASTLE_CLIENT_ID': '1234'}
    req.COOKIES = {}
    return req


class SessionTestCase(unittest.TestCase):
    def test_init(self):
        client = Client.from_request(request(), {})
        client2 = Client.from_request(request(), {})
        self.assertNotEqual(client.api.request, client2.api.request)
        self.assertEqual(client.api.req.sharer, client2.api.req.sharer)
