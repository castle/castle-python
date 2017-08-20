import responses
from collections import namedtuple

from castle.test import unittest
from castle.client import Client
from castle.configuration import configuration
from castle.api import Api


def request():
    request = namedtuple('Request', ['ip', 'environ'])
    request.ip = '217.144.192.112'
    request.environ = { 'HTTP_X_FORWARDED_FOR': '217.144.192.112', 'HTTP_X_CASTLE_CLIENT_ID': '1234' }
    return request


class ClientTestCase(unittest.TestCase):
    def test_init(self):
        context = {'active': True, 'client_id': '1234', 'headers': {'X-Forwarded-For': '217.144.192.112'}, 'ip': '217.144.192.112', 'library': {'name': 'castle-python', 'version': '0.1.0'}, 'origin': 'web'}
        client = Client(request(), {})
        self.assertEqual(client.options, {})
        self.assertEqual(client.do_not_track, False)
        self.assertEqual(client.context, context)
        self.assertIsInstance(client.api, Api)

    @responses.activate
    def test_identify_tracked_true(self):
        response_text = 'identify'
        responses.add(responses.POST, 'https://api.castle.io/v1/identify', json=response_text, status=200)
        client = Client(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.identify(options), response_text)

    def test_identify_tracked_false(self):
        client = Client(request(), {})
        client.disable_tracking()
        self.assertEqual(client.identify({}), None)

    @responses.activate
    def test_authenticate_tracked_true(self):
        response_text = 'authenticate'
        responses.add(responses.POST, 'https://api.castle.io/v1/authenticate', json=response_text, status=200)
        client = Client(request(), {})
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.authenticate(options), response_text)

    def test_authenticate_tracked_false(self):
        client = Client(request(), {})
        client.disable_tracking()
        options = {'event': '$login.authenticate', 'user_id': '1234'}
        self.assertEqual(client.authenticate(options), {'action': 'allow', 'user_id': '1234'})

    @responses.activate
    def test_track_tracked_true(self):
        response_text = 'track'
        responses.add(responses.POST, 'https://api.castle.io/v1/track', json=response_text, status=200)
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
        context = {'active': True, 'client_id': '1234', 'headers': {'X-Forwarded-For': '217.144.192.112'}, 'ip': '217.144.192.112', 'library': {'name': 'castle-python', 'version': '0.1.0'}, 'origin': 'web'}
        client = Client(request(), {})
        self.assertEqual(client.setup_context(request()), context)

    def test_failover_strategy_not_throw(self):
        client = Client(request(), {'user_id': '1234'})
        self.assertEqual(client.failover(Exception), {'action': 'allow', 'user_id': '1234'})

    def test_failover_strategy_throw(self):
        client = Client(request(), {'user_id': '1234'})
        configuration.failover_strategy = 'throw'
        with self.assertRaises(Exception):
            client.failover(Exception)
        configuration.failover_strategy = 'allow'
