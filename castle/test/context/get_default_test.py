from castle.test import unittest, mock

from castle.version import VERSION as __version__
from castle.context.get_default import ContextGetDefault


def client_id():
    return 'abcd'


def cookies():
    return {'__cid': client_id()}


def request_ip():
    return '5.5.5.5'


def environ():
    return {
        'HTTP_X_FORWARDED_FOR': request_ip(),
        'HTTP_COOKIE': "__cid={client_id()};other=efgh",
        'HTTP-Accept-Language': 'en',
        'HTTP-User-Agent': 'test'
    }


def request(env):
    req = mock.Mock()
    req.ip = request_ip()
    req.environ = env
    return req


class ContextGetDefaultTestCase(unittest.TestCase):

    def test_default_context(self):
        context = ContextGetDefault(
            request(environ()), cookies()).call()
        self.assertEqual(context['client_id'], client_id())
        self.assertEqual(context['active'], True)
        self.assertEqual(context['origin'], 'web')
        self.assertEqual(
            context['headers'],
            {
                'X-Forwarded-For': request_ip(),
                'Accept-Language': 'en',
                'User-Agent': 'test',
                'Cookie': True
            }
        )
        self.assertEqual(context['ip'], request_ip())
        self.assertDictEqual(
            context['library'],
            {'name': 'castle-python', 'version': __version__}
        )
        self.assertEqual(context['user_agent'], 'test')
