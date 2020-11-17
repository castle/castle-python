import json
import responses

from castle.test import unittest
from castle.api.get_device import APIGetDevice
from castle.configuration import configuration


class APIGetDeviceTestCase(unittest.TestCase):
    def setUp(self):
        configuration.api_secret = 'test'

    def tearDown(self):
        configuration.api_secret = None

    @responses.activate
    def test_retrieve(self):
        # pylint: disable=line-too-long
        response_text = "{\"id\":\"d_id\",\"manufacturer\":\"d_manufacturer\",\"model\":\"d_model\",\"name\":\"d_name\",\"type\":\"d_type\"}"
        responses.add(
            responses.GET,
            'https://api.castle.io/v1/devices/1234',
            body=response_text,
            status=200
        )
        device_token = '1234'
        self.assertEqual(APIGetDevice.retrieve(device_token), json.loads(response_text))
