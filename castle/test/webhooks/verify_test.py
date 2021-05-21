import requests

from castle.test import unittest
from castle.webhooks.verify import WebhooksVerify
from castle.errors import WebhookVerificationError


def webhook(signature):
    req = requests.Request(headers={"X-Castle-Signature": signature})
    str_dict = "{'user_traits': {}, 'policy': {}, 'data': {'location': {}, 'id': 'test', 'user_agent': {}, 'user_id': '', 'device_token': 'token', 'context': {}, 'trigger': '$login.succeeded'}, 'created_at': '2020-12-18T12:55:21.779Z', 'type': '$incident.confirmed', 'properties': {}}"
    req.data = bytes(str_dict.encode('utf-8'))
    return req


class WebhooksVerifyTestCase(unittest.TestCase):
    def test_webhook_malformed(self):
        with self.assertRaises(WebhookVerificationError):
            WebhooksVerify().call(webhook("123"))

    def test_webhook_valid(self):
        self.assertEqual(
            WebhooksVerify().call(webhook("v61Bn6ItuClDcRqrr6++csm2Ub3Jfyos4BMR3PslhBY=")),
            None
        )
