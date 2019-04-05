import json
from collections import namedtuple
import responses
from castle.test import mock, unittest
from castle.client import Client
from castle.configuration import configuration
from castle.exceptions import ImpersonationFailed
from castle.api import Api
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
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch('castle.client.generate_timestamp')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = '2018-01-02T03:04:05.678'
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = {
            'active': True,
            'client_id': '1234',
            'headers': {'User-Agent': 'test', 'X-Forwarded-For': '217.144.192.112'},
            'ip': '217.144.192.112',
            'library': {'name': 'castle-python', 'version': VERSION},
            'origin': 'web',
            'user_agent': 'test'
        }
        client = Client.from_request(request(), {})
        self.assertEqual(client.do_not_track, False)
        self.assertEqual(client.context, context)
        self.assertIsInstance(client.api, Api)

    @responses.activate
    def test_impersonate(self):
        response_text = {'success': True}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/impersonate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'impersonator': 'admin', 'user_id': '1234'}
        self.assertEqual(client.impersonate(options), response_text)

    @responses.activate
    def test_impersonate_failed(self):
        response_text = {}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/impersonate',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'impersonator': 'admin', 'user_id': '1234'}
        with self.assertRaises(ImpersonationFailed):
            client.impersonate(options)

    @responses.activate
    def test_identify_tracked_true(self):
        response_text = 'identify'
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/identify',
            json=response_text,
            status=200
        )
        client = Client.from_request(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.identify(options), response_text)

    def test_identify_tracked_false(self):
        client = Client.from_request(request(), {})
        client.disable_tracking()
        self.assertEqual(client.identify({}), None)

    @responses.activate
    def test_authenticate_tracked_true(self):
        response_text = {'action': 'allow', 'user_id': '1234'}
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
            'action': 'allow',
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
            'action': 'allow',
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

    def test_setup_client_id_from_cookies(self):
        cookies = {'__cid': '1234'}
        options = {'cookies': cookies}
        result_context = Client.to_context(request(), options)
        self.assertEqual(result_context['client_id'], '1234')

    def test_to_options(self):
        options = Client.to_options({'foo': 'bar'})
        self.assertEqual(
            options, {'foo': 'bar', 'timestamp': '2018-01-02T03:04:05.678'})

    def test_to_options_with_deprecation(self):
        options = Client.to_options({'foo': 'bar', 'traits': {}})
        self.assertEqual(
            options, {'foo': 'bar', 'timestamp': '2018-01-02T03:04:05.678', 'traits': {}})

    def test_to_context(self):
        context = {
            'active': True,
            'client_id': '1234',
            'headers': {'User-Agent': 'test', 'X-Forwarded-For': '217.144.192.112'},
            'ip': '217.144.192.112',
            'library': {'name': 'castle-python', 'version': VERSION},
            'origin': 'web',
            'user_agent': 'test'
        }
        result_context = Client.to_context(request(), {})
        self.assertEqual(result_context, context)

    def test_failover_strategy_not_throw(self):
        options = {'user_id': '1234'}
        self.assertEqual(
            Client.failover_response_or_raise(options, Exception()),
            {
                'action': 'allow',
                'user_id': '1234',
                'failover': True,
                'failover_reason': 'Exception'
            }
        )

    def test_failover_strategy_throw(self):
        options = {'user_id': '1234'}
        configuration.failover_strategy = 'throw'
        with self.assertRaises(Exception):
            Client.failover_response_or_raise(options, Exception())
        configuration.failover_strategy = 'allow'

    @responses.activate
    def test_timestamps_are_not_global(self):
        response_text = {'action': 'allow', 'user_id': '1234'}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text,
            status=200
        )
        options1 = {'event': '$login.authenticate', 'user_id': '1234'}
        options2 = {'event': '$login.authenticate', 'user_id': '1234'}
        client1 = Client.from_request(request())
        client1.authenticate(options1)
        self.mock_timestamp.return_value = '2018-01-02T04:04:05.678'
        client2 = Client.from_request(request())
        client2.authenticate(options2)

        response_body1 = json.loads(responses.calls[0].request.body)
        response_body2 = json.loads(responses.calls[1].request.body)

        self.assertNotEqual(response_body1['timestamp'], response_body2['timestamp'])
