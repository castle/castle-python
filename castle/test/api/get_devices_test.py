import json
import responses

from castle.test import unittest
from castle.api.get_devices import APIGetDevices
from castle.configuration import configuration


class APIGetDevicesTestCase(unittest.TestCase):
    def setUp(self):
        configuration.api_secret = 'test'

    def tearDown(self):
        configuration.api_secret = None

    @responses.activate
    def test_retrieve(self):
        # pylint: disable=line-too-long
        response_text = "{\"total_count\":1,\"data\":[{\"token\":\"abcdefg12345\",\"risk\":0.0,\"created_at\":\"2018-06-15T16:36:22.916Z\",\"last_seen_at\":\"2018-07-19T23:09:29.681Z\",\"context\":{\"ip\":\"1.1.1.1\",\"user_agent\":{\"raw\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.51\",\"browser\":\"Opera\",\"version\":\"54.0.2952\",\"os\":\"Mac OS X 10.13.6\",\"mobile\":false,\"platform\":\"Mac OS X\",\"device\":\"Unknown\",\"family\":\"Opera\"},\"type\":\"desktop\"},\"is_current_device\":true}]}"
        responses.add(
            responses.GET,
            'https://api.castle.io/v1/users/1234/devices',
            body=response_text,
            status=200
        )
        user_id = '1234'
        self.assertEqual(APIGetDevices.retrieve(user_id), json.loads(response_text))
