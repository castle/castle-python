from requests import Response
import responses

from castle.test import unittest
from castle.api_request import APIRequest
from castle.command import Command
from castle.core.send_request import CoreSendRequest
from castle.configuration import configuration, Configuration
from castle.errors import ConfigurationError


def command():
    return Command(method='post', path='authenticate', data={})


def response_text():
    return 'authenticate'


class APIRequestTestCase(unittest.TestCase):
    def setUp(self):
        configuration.api_secret = 'test'

    def tearDown(self):
        configuration.api_secret = None

    def test_init(self):
        self.assertIsInstance(APIRequest().req, CoreSendRequest)

    def test_init_custom_config(self):
        cfg = Configuration()
        self.assertIsInstance(APIRequest(cfg).req, CoreSendRequest)

    @responses.activate
    def test_request(self):
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text(),
            status=200
        )
        self.assertIsInstance(APIRequest().request(command()), Response)

    @responses.activate
    def test_call(self):
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text(),
            status=200
        )
        self.assertEqual(APIRequest().call(command()), response_text())

    @responses.activate
    def test_no_api_secret(self):
        configuration.api_secret = ''
        with self.assertRaises(ConfigurationError):
            APIRequest().call(command())
