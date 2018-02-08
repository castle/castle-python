from castle.test import unittest, mock

from castle.version import VERSION as __version__
from castle.context.default import ContextDefault


def client_id():
    return 'abcd'


def cookies():
    return {'__cid': client_id()}


def request_ip():
    return '127.0.0.1'


def environ():
    return {
        'HTTP_X_FORWARDED_FOR': request_ip(),
        'HTTP_COOKIE': "__cid={client_id()};other=efgh"
    }


def environ_with_extras():
    extra = {
        'HTTP-Accept-Language': 'en',
        'HTTP-User-Agent': 'test'
    }
    context = dict(environ())
    context.update(extra)
    return context


def request(env):
    req = mock.Mock()
    req.ip = request_ip()
    req.environ = env
    return req


class ContextDefaultTestCase(unittest.TestCase):
    def test_default_context(self):
        context = ContextDefault(request(environ()), cookies()).call()
        self.assertEqual(context['client_id'], client_id())
        self.assertEqual(context['active'], True)
        self.assertEqual(context['origin'], 'web')
        self.assertEqual(context['headers'], {'X-Forwarded-For': request_ip()})
        self.assertEqual(context['ip'], request_ip())
        self.assertDictEqual(context['library'], {
                             'name': 'castle-python', 'version': __version__})

    def test_default_context_with_extras(self):
        context = ContextDefault(
            request(environ_with_extras()), cookies()).call()
        self.assertEqual(context['client_id'], client_id())
        self.assertEqual(context['active'], True)
        self.assertEqual(context['origin'], 'web')
        self.assertEqual(
            context['headers'],
            {'X-Forwarded-For': request_ip(), 'Accept-Language': 'en',
             'User-Agent': 'test'}
        )
        self.assertEqual(context['ip'], request_ip())
        self.assertDictEqual(
            context['library'],
            {'name': 'castle-python', 'version': __version__}
        )
