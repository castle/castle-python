import json
import responses

from castle.test import unittest
from castle.api.get_devices_for_user import APIGetDevicesForUser
from castle.configuration import configuration


class APIGetDevicesForUserTestCase(unittest.TestCase):
    def setUp(self):
        configuration.api_secret = 'test'

    def tearDown(self):
        configuration.api_secret = None

    @responses.activate
    def test_call(self):
        # pylint: disable=line-too-long
        response_text = "{\"total_count\":2,\"data\":[{\"token\":\"token\",\"created_at\":\"2020-08-01T18:55:45.352Z\",\"last_seen_at\":\"2020-10-18T21:11:57.476Z\",\"user_id\":\"4\",\"approved_at\":\"2020-08-13T09:55:19.286Z\",\"escalated_at\":null,\"mitigated_at\":null,\"context\":{\"ip\":\"127.0.0.1\",\"location\":{\"country_code\":\"PL\",\"country\":\"Poland\"},\"user_agent\":{\"raw\":\"Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/86.0.4240.75 Safari\\/537.36\",\"browser\":\"Chrome\",\"version\":\"86.0.4240\",\"os\":\"Mac OS X 10.15.6\",\"mobile\":false,\"platform\":\"Mac OS X\",\"device\":\"Mac\",\"family\":\"Chrome\"},\"properties\":{},\"type\":\"desktop\"},\"is_current_device\":false},{\"token\":\"token2\",\"created_at\":\"2020-08-13T11:26:47.401Z\",\"last_seen_at\":\"2020-10-18T18:37:22.855Z\",\"user_id\":\"4\",\"approved_at\":null,\"escalated_at\":null,\"mitigated_at\":null,\"context\":{\"ip\":\"127.0.0.1\",\"location\":{\"country_code\":\"PL\",\"country\":\"Poland\"},\"user_agent\":{\"raw\":\"Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/86.0.4240.75 Safari\\/537.36\",\"browser\":\"Chrome\",\"version\":\"86.0.4240\",\"os\":\"Mac OS X 10.15.6\",\"mobile\":false,\"platform\":\"Mac OS X\",\"device\":\"Mac\",\"family\":\"Chrome\"},\"properties\":{},\"type\":\"desktop\"},\"is_current_device\":false}]}"
        responses.add(
            responses.GET,
            'https://api.castle.io/v1/users/1234/devices',
            body=response_text,
            status=200
        )
        user_id = '1234'
        self.assertEqual(APIGetDevicesForUser.call(user_id), json.loads(response_text))
