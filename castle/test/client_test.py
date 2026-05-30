from collections import namedtuple
import responses
from castle.api_request import APIRequest
from castle.client import Client
from castle.configuration import configuration
from castle.failover.strategy import FailoverStrategy
from castle.test import unittest
from castle.verdict import Verdict
from castle.version import VERSION


def request():
    req = namedtuple('Request', ['ip', 'environ', 'COOKIES'])
    req.ip = '217.144.192.112'
    req.environ = {
        'HTTP_X_FORWARDED_FOR': '217.144.192.112',
        'HTTP-User-Agent': 'test',
        'HTTP_X_CASTLE_CLIENT_ID': '1234',
    }
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
            'client_id': '1234',
            'headers': {
                'User-Agent': 'test',
                'X-Forwarded-For': '217.144.192.112',
                'X-Castle-Client-Id': '1234',
            },
            'ip': '217.144.192.112',
            'library': {'name': 'castle-python', 'version': VERSION},
            'user_agent': 'test',
        }
        client = Client.from_request(request(), {})
        self.assertEqual(client.do_not_track, False)
        self.assertEqual(client.context, context)
        self.assertIsInstance(client.api, APIRequest)

    @responses.activate
    def test_filter_tracked_true(self):
        response_text = {'action': Verdict.ALLOW.value, 'user_id': '1234'}
        responses.add(
            responses.POST, 'https://api.castle.io/v1/filter', json=response_text, status=200
        )
        client = Client.from_request(request(), {})
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        response_text.update(failover=False, failover_reason=None)
        self.assertEqual(client.filter(options), response_text)

    @responses.activate
    def test_filter_tracked_true_status_500(self):
        response_text = {
            'policy': {'action': Verdict.ALLOW.value},
            'action': Verdict.ALLOW.value,
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'InternalServerError',
        }
        responses.add(responses.POST, 'https://api.castle.io/v1/filter', json='filter', status=500)
        client = Client.from_request(request(), {})
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        self.assertEqual(client.filter(options), response_text)

    @responses.activate
    def test_filter_tracked_true_status_500_without_user(self):
        # `user` is optional on /v1/filter (#279) - it must not crash on failover
        response_text = {
            'policy': {'action': Verdict.ALLOW.value},
            'action': Verdict.ALLOW.value,
            'user_id': 'matching-1234',
            'failover': True,
            'failover_reason': 'InternalServerError',
        }
        responses.add(responses.POST, 'https://api.castle.io/v1/filter', json='filter', status=500)
        client = Client.from_request(request(), {})
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'matching_user_id': 'matching-1234',
        }
        self.assertEqual(client.filter(options), response_text)

    def test_filter_tracked_false(self):
        response_text = {
            'policy': {'action': Verdict.ALLOW.value},
            'action': Verdict.ALLOW.value,
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'Castle set to do not track.',
        }
        client = Client.from_request(request(), {})
        client.disable_tracking()
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        self.assertEqual(client.filter(options), response_text)

    @responses.activate
    def test_log_tracked_true(self):
        response_text = 'log'
        responses.add(
            responses.POST, 'https://api.castle.io/v1/log', json=response_text, status=200
        )
        client = Client.from_request(request(), {})
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        self.assertEqual(client.log(options), response_text)

    def test_log_tracked_false(self):
        client = Client.from_request(request(), {})
        client.disable_tracking()
        self.assertEqual(client.log({}), None)

    @responses.activate
    def test_risk_tracked_true(self):
        response_text = {'action': Verdict.ALLOW.value, 'user_id': '1234'}
        responses.add(
            responses.POST, 'https://api.castle.io/v1/risk', json=response_text, status=200
        )
        client = Client.from_request(request(), {})
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        response_text.update(failover=False, failover_reason=None)
        self.assertEqual(client.risk(options), response_text)

    @responses.activate
    def test_risk_tracked_true_status_500(self):
        response_text = {
            'policy': {'action': Verdict.ALLOW.value},
            'action': Verdict.ALLOW.value,
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'InternalServerError',
        }
        responses.add(responses.POST, 'https://api.castle.io/v1/risk', json='risk', status=500)
        client = Client.from_request(request(), {})
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        self.assertEqual(client.risk(options), response_text)

    def test_risk_tracked_false(self):
        response_text = {
            'policy': {'action': Verdict.ALLOW.value},
            'action': Verdict.ALLOW.value,
            'user_id': '1234',
            'failover': True,
            'failover_reason': 'Castle set to do not track.',
        }
        client = Client.from_request(request(), {})
        client.disable_tracking()
        options = {
            'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
            'event': '$login',
            'status': '$succeeded',
            'user': {'id': '1234'},
        }
        self.assertEqual(client.risk(options), response_text)

    @responses.activate
    def test_create_list(self):
        response_text = {'id': 'list-id', 'name': 'my-list'}
        responses.add(
            responses.POST, 'https://api.castle.io/v1/lists', json=response_text, status=201
        )
        client = Client.from_request(request(), {})
        options = {'name': 'my-list', 'color': '$grey', 'primary_field': 'user.email'}
        self.assertEqual(client.create_list(options), response_text)

    @responses.activate
    def test_get_list(self):
        response_text = {'id': 'list-id', 'name': 'my-list'}
        responses.add(
            responses.GET, 'https://api.castle.io/v1/lists/list-id', json=response_text, status=200
        )
        client = Client.from_request(request(), {})
        self.assertEqual(client.get_list({'list_id': 'list-id'}), response_text)

    @responses.activate
    def test_delete_list(self):
        responses.add(
            responses.DELETE, 'https://api.castle.io/v1/lists/list-id', json={}, status=200
        )
        client = Client.from_request(request(), {})
        self.assertEqual(client.delete_list({'list_id': 'list-id'}), {})

    @responses.activate
    def test_create_batch_list_items(self):
        response_text = {'items': []}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/lists/list-id/items/batch',
            json=response_text,
            status=201,
        )
        client = Client.from_request(request(), {})
        options = {'list_id': 'list-id', 'items': [{'primary_value': 'a@b.com'}]}
        self.assertEqual(client.create_batch_list_items(options), response_text)

    @responses.activate
    def test_request_user_data(self):
        response_text = {'status': 'queued'}
        responses.add(
            responses.POST, 'https://api.castle.io/v1/privacy/users', json=response_text, status=200
        )
        client = Client.from_request(request(), {})
        options = {'identifier': 'a@b.com', 'identifier_type': '$email'}
        self.assertEqual(client.request_user_data(options), response_text)

    @responses.activate
    def test_delete_user_data(self):
        response_text = {'status': 'queued'}
        responses.add(
            responses.DELETE,
            'https://api.castle.io/v1/privacy/users',
            json=response_text,
            status=200,
        )
        client = Client.from_request(request(), {})
        options = {'identifier': 'a@b.com', 'identifier_type': '$email'}
        self.assertEqual(client.delete_user_data(options), response_text)

    @responses.activate
    def test_events_schema(self):
        response_text = {'fields': []}
        responses.add(
            responses.GET,
            'https://api.castle.io/v1/events/schema',
            json=response_text,
            status=200,
        )
        client = Client.from_request(request(), {})
        self.assertEqual(client.events_schema(), response_text)

    @responses.activate
    def test_query_events(self):
        response_text = {'data': []}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/events/query',
            json=response_text,
            status=200,
        )
        client = Client.from_request(request(), {})
        self.assertEqual(client.query_events({'filters': []}), response_text)

    @responses.activate
    def test_group_events(self):
        response_text = {'data': []}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/events/group',
            json=response_text,
            status=200,
        )
        client = Client.from_request(request(), {})
        self.assertEqual(client.group_events({'filters': []}), response_text)

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
            Client.failover_response_or_raise(options.get('user_id'), Exception()),
            {
                'policy': {'action': Verdict.ALLOW.value},
                'action': Verdict.ALLOW.value,
                'user_id': '1234',
                'failover': True,
                'failover_reason': 'Exception',
            },
        )

    def test_failover_strategy_throw(self):
        options = {'user_id': '1234'}
        configuration.failover_strategy = FailoverStrategy.THROW.value
        with self.assertRaises(Exception):
            Client.failover_response_or_raise(options, Exception())
        configuration.failover_strategy = FailoverStrategy.ALLOW.value
