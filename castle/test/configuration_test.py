from castle.test import unittest
from castle.exceptions import ConfigurationError
from castle.configuration import Configuration, BLACK_LIST
from castle.headers_formatter import HeadersFormatter


class ConfigurationTestCase(unittest.TestCase):
    def test_default_values(self):
        config = Configuration()
        self.assertEqual(config.api_secret, None)
        self.assertEqual(config.host, 'api.castle.io')
        self.assertEqual(config.port, 443)
        self.assertEqual(config.url_prefix, '/v1')
        self.assertEqual(config.white_list, [])
        self.assertEqual(config.black_list, [])
        self.assertEqual(config.request_timeout, 500)
        self.assertEqual(config.failover_strategy, 'allow')

    def test_api_secret_setter(self):
        config = Configuration()
        config.api_secret = 'test'
        self.assertEqual(config.api_secret, 'test')

    def test_host_setter(self):
        config = Configuration()
        config.host = 'test'
        self.assertEqual(config.host, 'test')

    def test_port_setter(self):
        config = Configuration()
        config.port = 80
        self.assertEqual(config.port, 80)

    def test_url_prefix_setter(self):
        config = Configuration()
        config.url_prefix = '/v2'
        self.assertEqual(config.url_prefix, '/v2')

    def test_white_list_setter_list(self):
        config = Configuration()
        config.white_list = ['test']
        self.assertEqual(config.white_list, ['Test'])

    def test_white_list_setter_none(self):
        config = Configuration()
        config.white_list = None
        self.assertEqual(config.white_list, [])

    def test_white_list_setter_empty(self):
        config = Configuration()
        config.white_list = ''
        self.assertEqual(config.white_list, [])

    def test_black_list_setter_list(self):
        config = Configuration()
        config.black_list = ['test']
        self.assertEqual(config.black_list, ['Test'])

    def test_black_list_setter_none(self):
        config = Configuration()
        config.black_list = None
        self.assertEqual(config.black_list, [])

    def test_black_list_setter_empty(self):
        config = Configuration()
        config.black_list = ''
        self.assertEqual(config.black_list, [])

    def test_request_timeout_setter(self):
        config = Configuration()
        config.request_timeout = 5000
        self.assertEqual(config.request_timeout, 5000)

    def test_failover_strategy_setter_valid(self):
        config = Configuration()
        config.failover_strategy = 'throw'
        self.assertEqual(config.failover_strategy, 'throw')

    def test_failover_strategy_setter_invalid(self):
        config = Configuration()
        with self.assertRaises(ConfigurationError):
            config.failover_strategy = 'invalid'
