from castle.test import unittest, mock

from castle.version import VERSION as __version__
from castle.configuration import configuration
from castle.context.default import ContextDefault


class ContextDefaultTestCase(unittest.TestCase):
    def client_id(self):
        return 'abcd'

    def cookies(self):
        return { '__cid': self.client_id() }

    def request_ip(self):
        return '127.0.0.1'

    def environ(self):
        return {
            'HTTP_X_FORWARDED_FOR': self.request_ip(),
            'HTTP_COOKIE': "__cid={self.client_id()};other=efgh"
        }

    def environ_with_extras(self):
        extra = {
            'HTTP-Accept-Language': 'en',
            'HTTP-User-Agent': 'test'
        }
        context = dict(self.environ())
        context.update(extra)
        return context

    def request(self, environ):
        r = mock.Mock()
        r.ip = self.request_ip
        r.environ = environ
        return r

    def test_default_context(self):
        context = ContextDefault(self.request(self.environ()), self.cookies()).call()
        self.assertEqual(context['client_id'], self.client_id())
        self.assertEqual(context['active'], True)
        self.assertEqual(context['origin'], 'web')
        self.assertEqual(context['headers'], { 'X-Forwarded-For': self.request_ip() })
        self.assertEqual(context['ip'], self.request_ip())
        self.assertDictEqual(context['library'], { 'name': 'castle-python', 'version': __version__ })

    def test_default_context_with_extras(self):
        context = ContextDefault(self.request(self.environ_with_extras()), self.cookies()).call()
        self.assertEqual(context['client_id'], self.client_id())
        self.assertEqual(context['active'], True)
        self.assertEqual(context['origin'], 'web')
        self.assertEqual(context['headers'], { 'X-Forwarded-For': self.request_ip(), 'Accept-Language': 'en', 'User-Agent': 'test' })
        self.assertEqual(context['ip'], self.request_ip())
        self.assertDictEqual(context['library'], { 'name': 'castle-python', 'version': __version__ })
