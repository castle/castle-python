from collections import namedtuple
import responses

from castle.test import unittest
from castle.client import Client
from castle.configuration import configuration
from castle.api import Api
from castle.version import VERSION


def request():
    req = namedtuple('Request', ['ip', 'environ'])
    req.ip = '217.144.192.112'
    req.environ = {'HTTP_X_FORWARDED_FOR': '217.144.192.112', 'HTTP_X_CASTLE_CLIENT_ID': '1234'}
    return req


class ClientTestCase(unittest.TestCase):
    def test_init(self):
        context = {
            'active': True,
            'client_id': '1234',
            'headers': {'X-Forwarded-For': '217.144.192.112'},
            'ip': '217.144.192.112',
            'library': {'name': 'castle-python', 'version': VERSION},
            'origin': 'web'
        }
        client = Client(request(), {})
        self.assertEqual(client.options, {})
        self.assertEqual(client.do_not_track, False)
        self.assertEqual(client.context, context)
        self.assertIsInstance(client.api, Api)

    @responses.activate
    def test_identify_tracked_true(self):
        response_text = 'identify'
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/identify',
            json=response_text,
            status=200
        )
        client = Client(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.identify(options), response_text)

    def test_identify_tracked_false(self):
        client = Client(request(), {})
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
        client = Client(request(), {})
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
        client = Client(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.authenticate(options), response_text)

    def test_authenticate_tracked_false(self):
        response_text = {
            'action': 'allow',
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'Castle set to do not track.'
        }
        client = Client(request(), {})
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
        client = Client(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.track(options), response_text)

    def test_track_tracked_false(self):
        client = Client(request(), {})
        client.disable_tracking()
        self.assertEqual(client.track({}), None)

    def test_disable_tracking(self):
        client = Client(request(), {})
        client.disable_tracking()
        self.assertEqual(client.do_not_track, True)

    def test_enable_tracking(self):
        client = Client(request(), {})
        client.disable_tracking()
        self.assertEqual(client.do_not_track, True)
        client.enable_tracking()
        self.assertEqual(client.do_not_track, False)

    def test_tracked_true(self):
        client = Client(request(), {})
        self.assertEqual(client.tracked(), True)

    def test_tracked_false(self):
        client = Client(request(), {})
        client.disable_tracking()
        self.assertEqual(client.tracked(), False)

    def test_default_tracking_true(self):
        client = Client(request(), {'do_not_track': True})
        self.assertEqual(client.default_tracking(), True)

    def test_default_tracking_false(self):
        client = Client(request(), {})
        self.assertEqual(client.default_tracking(), False)

    def test_setup_context(self):
        context = {
            'active': True,
            'client_id': '1234',
            'headers': {'X-Forwarded-For': '217.144.192.112'},
            'ip': '217.144.192.112',
            'library': {'name': 'castle-python', 'version': VERSION},
            'origin': 'web'
        }
        client = Client(request(), {})
        self.assertEqual(client.setup_context(request()), context)

    def test_failover_strategy_not_throw(self):
        options = {'user_id': '1234'}
        client = Client(request(), options)
        self.assertEqual(
            client.failover(options, Exception()),
            {
                'action': 'allow',
                'user_id': '1234',
                'failover': True,
                'failover_reason': 'Exception'
            }
        )

    def test_failover_strategy_throw(self):
        options = {'user_id': '1234'}
        client = Client(request(), options)
        configuration.failover_strategy = 'throw'
        with self.assertRaises(Exception):
            client.failover(options, Exception())
        configuration.failover_strategy = 'allow'
