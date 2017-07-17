import responses
from requests import Response

from castle.test import unittest, mock
from castle.request import Request
from castle.configuration import configuration


class RequestTestCase(unittest.TestCase):
    def test_init_headers(self):
        headers = {'X-Castle-Client-Id': '1234'}
        self.assertEqual(Request(headers).headers, headers)

    def test_init_base_url(self):
        self.assertEqual(Request().base_url, 'https://api.castle.io/v1')

    @responses.activate
    def test_build_query(self):
        data = {'event': '$login.authenticate', 'user_id': '12345'}
        configuration.api_secret = 'api_secret'
        # JSON requires double quotes for its strings
        response_text = {"action": "allow", "user_id": "12345"}
        responses.add(responses.POST, 'https://api.castle.io/v1/authenticate', json=response_text, status=200)
        res = Request().build_query('post', 'authenticate', data)
        self.assertIsInstance(res, Response)
        self.assertIsInstance(res.text, str)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), response_text)
        configuration.api_secret = None

    def test_build_url(self):
        self.assertEqual(Request().build_url('authenticate'), 'https://api.castle.io/v1/authenticate')

    def test_build_url_remove_slash(self):
        self.assertEqual(Request().build_url('/authenticate'), 'https://api.castle.io/v1/authenticate')

    def test_verify_true(self):
        self.assertEqual(Request().verify(), True)

    def test_verify_false(self):
        configuration.port = 3001
        self.assertEqual(Request().verify(), False)
        configuration.port = 443
