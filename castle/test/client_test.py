from collections import namedtuple
import responses
from castle.api_request import APIRequest
from castle.client import Client
from castle.configuration import configuration
from castle.errors import ImpersonationFailed
from castle.failover.strategy import FailoverStrategy
from castle.test import unittest
from castle.verdict import Verdict
from castle.version import VERSION


def request():
    req = namedtuple('Request', ['ip', 'environ', 'COOKIES'])
    req.ip = '217.144.192.112'
    req.environ = {'HTTP_X_FORWARDED_FOR': '217.144.192.112',
                   'HTTP-User-Agent': 'test',
                   'HTTP_X_CASTLE_CLIENT_ID': '1234'}
    req.COOKIES = {}
    return req


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        configuration.api_secret = 'test'

    def tearDown(self):
        configuration.api_secret = None

    def test_init(self):
        context = {
            'active': True,
            'library': {'name': 'castle-python', 'version': VERSION}
        }
        client = Client.from_request(request(), {})
        default_options = {
            'fingerprint': '1234',
            'headers': {
                'X-Forwarded-For': '217.144.192.112',
                'User-Agent': 'test',
                'X-Castle-Client-Id': '1234'
            },
            'ip': '217.144.192.112',
            'context': {'active': True, 'library': {'name': 'castle-python', 'version': VERSION}}
        }
        self.assertEqual(client.default_options, default_options)
        self.assertEqual(client.do_not_track, False)
        self.assertEqual(client.context, context)
        self.assertIsInstance(client.api, APIRequest)

    @responses.activate
    def test_start_impersonation(self):
        response_text = {'success': True}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/impersonate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'properties': {'impersonator': 'admin'}, 'user_id': '1234'}
        self.assertEqual(client.start_impersonation(options), response_text)

    @responses.activate
    def test_end_impersonation(self):
        response_text = {'success': True}
        responses.add(
            responses.DELETE,
            'https://api.castle.io/v1/impersonate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'properties': {'impersonator': 'admin'}, 'user_id': '1234'}
        self.assertEqual(client.end_impersonation(options), response_text)

    @responses.activate
    def test_start_impersonation_failed(self):
        response_text = {}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/impersonate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'properties': {'impersonator': 'admin'}, 'user_id': '1234'}
        with self.assertRaises(ImpersonationFailed):
            client.start_impersonation(options)

    @responses.activate
    def test_end_impersonation_failed(self):
        response_text = {}
        responses.add(
            responses.DELETE,
            'https://api.castle.io/v1/impersonate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'properties': {'impersonator': 'admin'}, 'user_id': '1234'}
        with self.assertRaises(ImpersonationFailed):
            client.end_impersonation(options)

    @responses.activate
    def test_authenticate_tracked_true(self):
        response_text = {'action': Verdict.ALLOW.value, 'user_id': '1234'}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        response_text.update(failover=False, failover_reason=None)
        self.assertEqual(client.authenticate(options), response_text)

    @responses.activate
    def test_authenticate_tracked_true_status_500(self):
        response_text = {
            'action': Verdict.ALLOW.value,
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'InternalServerError'
        }
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json='authenticate',
            status=500
        )
        client = Client.from_request(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.authenticate(options), response_text)

    def test_authenticate_tracked_false(self):
        response_text = {
            'action': Verdict.ALLOW.value,
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'Castle set to do not track.'
        }
        client = Client.from_request(request(), {})
        client.disable_tracking()
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.authenticate(options), response_text)

    @responses.activate
    def test_track_tracked_true(self):
        response_text = 'track'
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/track',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.track(options), response_text)

    def test_track_tracked_false(self):
        client = Client.from_request(request(), {})
        client.disable_tracking()
        self.assertEqual(client.track({}), None)

    def test_disable_tracking(self):
        client = Client.from_request(request(), {})
        client.disable_tracking()
        self.assertEqual(client.do_not_track, True)

    def test_enable_tracking(self):
        client = Client.from_request(request(), {})
        client.disable_tracking()
        self.assertEqual(client.do_not_track, True)
        client.enable_tracking()
        self.assertEqual(client.do_not_track, False)

    def test_tracked_when_do_not_track_false(self):
        client = Client.from_request(request(), {})
        self.assertEqual(client.tracked(), True)

    def test_tracked_when_do_not_track_true(self):
        client = Client.from_request(request(), {'do_not_track': True})
        self.assertEqual(client.tracked(), False)

    def test_failover_strategy_not_throw(self):
        options = {'user_id': '1234'}
        self.assertEqual(
            Client.failover_response_or_raise(options, Exception()),
            {
                'action': Verdict.ALLOW.value,
                'user_id': '1234',
                'failover': True,
                'failover_reason': 'Exception'
            }
        )

    def test_failover_strategy_throw(self):
        options = {'user_id': '1234'}
        configuration.failover_strategy = FailoverStrategy.THROW.value
        with self.assertRaises(Exception):
            Client.failover_response_or_raise(options, Exception())
        configuration.failover_strategy = FailoverStrategy.ALLOW.value
