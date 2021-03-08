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


def res():
    return {
        'foo': 'bar',
        'fingerprint': '1234',
        'headers': {
            'X-Forwarded-For': '217.144.192.112',
            'User-Agent': 'test',
            'X-Castle-Client-Id': '1234'
        },
        'ip': '217.144.192.112',
        'context': {'active': True, 'library': {'name': 'castle-python', 'version': '5.0.1'}},
        'timestamp': '2018-01-02T03:04:05.678'
    }


def resWithDeprecation():
    return {
        'foo': 'bar',
        'traits': {},
        'fingerprint': '1234',
        'headers': {
            'X-Forwarded-For': '217.144.192.112',
            'User-Agent': 'test',
            'X-Castle-Client-Id': '1234'
        },
        'ip': '217.144.192.112',
        'context': {'active': True, 'library': {'name': 'castle-python', 'version': '5.0.1'}},
        'timestamp': '2018-01-02T03:04:05.678'
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

        self.assertEqual(options, res())

    def test_call_with_deprecation(self):
        options = PayloadPrepare.call({'foo': 'bar', 'traits': {}}, request())

        self.assertEqual(options, resWithDeprecation())
