from castle.test import unittest, mock

from castle.version import VERSION as __version__
from castle.options.get_default import OptionsGetDefault


def fingerprint():
    return 'abcd'


def cookies():
    return {'__cid': fingerprint()}


def request_ip():
    return '5.5.5.5'


def environ():
    return {
        'HTTP_X_FORWARDED_FOR': request_ip(),
        'HTTP_COOKIE': "__cid={fingerprint()};other=efgh",
        'HTTP-Accept-Language': 'en',
        'HTTP-User-Agent': 'test'
    }


def request(env):
    req = mock.Mock()
    req.ip = request_ip()
    req.environ = env
    return req


class OptionsGetDefaultTestCase(unittest.TestCase):

    def test_default_context(self):
        opts = OptionsGetDefault(
            request(environ()), cookies()).call()
        self.assertEqual(opts['fingerprint'], fingerprint())
        self.assertEqual(
            opts['headers'],
            {
                'X-Forwarded-For': request_ip(),
                'Accept-Language': 'en',
                'User-Agent': 'test',
                'Cookie': True
            }
        )
        self.assertEqual(opts['ip'], request_ip())
