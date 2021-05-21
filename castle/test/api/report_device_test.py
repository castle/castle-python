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
    def test_call(self):
        # pylint: disable=line-too-long
        response_text = "{\"token\":\"token\",\"created_at\":\"2020-08-13T11:26:47.401Z\",\"last_seen_at\":\"2020-10-18T18:37:22.855Z\",\"user_id\":\"4\",\"approved_at\":\"2020-11-18T12:48:41.112Z\",\"escalated_at\":null,\"mitigated_at\":null,\"context\":{\"ip\":\"127.0.0.1\",\"location\":{\"country_code\":\"PL\",\"country\":\"Poland\"},\"user_agent\":{\"raw\":\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/86.0.4240.75 Safari\/537.36\",\"browser\":\"Chrome\",\"version\":\"86.0.4240\",\"os\":\"Mac OS X 10.15.6\",\"mobile\":false,\"platform\":\"Mac OS X\",\"device\":\"Mac\",\"family\":\"Chrome\"},\"properties\":{},\"type\":\"desktop\"},\"is_current_device\":false}"
        responses.add(
            responses.PUT,
            'https://api.castle.io/v1/devices/1234/report',
            body=response_text,
            status=200
        )
        device_token = '1234'
        self.assertEqual(APIReportDevice.call(device_token), json.loads(response_text))
