from collections import namedtuple
from castle.payload.prepare import PayloadPrepare
from castle.test import mock, unittest
from castle.version import VERSION


def request():
    req = namedtuple('Request', ['ip', 'environ', 'COOKIES'])
    req.ip = '217.144.192.112'
    req.environ = {'HTTP_X_FORWARDED_FOR': '217.144.192.112',
                   'HTTP-User-Agent': 'test',
                   'HTTP_X_CASTLE_CLIENT_ID': '1234'}
    req.COOKIES = {}
    return req


def ctx():
    return {
        'active': True,
        'library': {'name': 'castle-python', 'version': VERSION}
    }


class ContextPrepareTestCase(unittest.TestCase):
    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch('castle.payload.prepare.generate_timestamp.call')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = '2018-01-02T03:04:05.678'
        self.addCleanup(timestamp_patcher.stop)

    def test_call(self):
        options = PayloadPrepare.call({'foo': 'bar'}, request())
        self.assertEqual(
            options, {'foo': 'bar', 'timestamp': '2018-01-02T03:04:05.678', 'context': ctx()})

    def test_call_with_deprecation(self):
        options = PayloadPrepare.call({'foo': 'bar', 'traits': {}}, request())
        self.assertEqual(
            options, {'foo': 'bar', 'timestamp': '2018-01-02T03:04:05.678', 'traits': {}, 'context': ctx()})
