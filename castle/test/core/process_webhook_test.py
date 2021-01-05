import requests

from castle.test import unittest
from castle.core.process_webhook import CoreProcessWebhook
from castle.errors import APIError


def webhook(data=None):
    req = requests.Request()
    req.data = None if data is None else bytes(data)
    return req


class CoreProcessResponseTestCase(unittest.TestCase):
    def test_webhook_none(self):
        with self.assertRaises(APIError):
            CoreProcessWebhook(webhook()).call()

    def test_webhook_empty(self):
        with self.assertRaises(APIError):
            CoreProcessWebhook(webhook(data=b'')).call()

    def test_webhook_valid(self):
        data_stream = str({
            'type': '$incident.confirmed',
            'created_at': '2020-12-18T12:55:21.779Z',
            'data': {
                'id': 'test',
                'device_token': 'token',
                'user_id': '',
                'trigger': '$login.succeeded',
                'context': {},
                'location': {},
                'user_agent': {}
            },
            'user_traits': {},
            'properties': {},
            'policy': {}
        }).encode('utf-8')

        self.assertEqual(
            CoreProcessWebhook(
                webhook(data=data_stream)).call(),
            data_stream
        )
