import json
import responses

from castle.test import unittest
from castle.api.report_device import APIReportDevice
from castle.configuration import configuration


class APIReportDeviceTestCase(unittest.TestCase):
    def setUp(self):
        configuration.api_secret = 'test'

    def tearDown(self):
        configuration.api_secret = None

    @responses.activate
    def test_retrieve(self):
        # pylint: disable=line-too-long
        response_text = "{\"token\":\"1234\",\"risk\":\"0.0\",\"escalated_at\":\"2020-11-18T03:04:05.678\"}"
        responses.add(
            responses.PUT,
            'https://api.castle.io/v1/devices/1234/report',
            body=response_text,
            status=200
        )
        device_token = '1234'
        self.assertEqual(APIReportDevice.retrieve(device_token), json.loads(response_text))
