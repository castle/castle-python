from castle.test import unittest
from castle.exceptions import ConfigurationError
from castle.configuration import Configuration
from castle.headers_formatter import HeadersFormatter


class ConfigurationTestCase(unittest.TestCase):
    def test_default_values(self):
        config = Configuration()
        self.assertEqual(config.api_secret, None)
        self.assertEqual(config.host, 'api.castle.io')
        self.assertEqual(config.port, 443)
        self.assertEqual(config.url_prefix, '/v1')
        self.assertEqual(config.whitelisted, [])
        self.assertEqual(config.blacklisted, [])
        self.assertEqual(config.request_timeout, 500)
        self.assertEqual(config.failover_strategy, 'allow')
        self.assertEqual(config.ip_headers, [])
        self.assertEqual(config.trusted_proxies, [])

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

    def test_whitelisted_setter_list(self):
        config = Configuration()
        config.whitelisted = ['test']
        self.assertEqual(config.whitelisted, ['Test'])

    def test_whitelisted_setter_none(self):
        config = Configuration()
        config.whitelisted = None
        self.assertEqual(config.whitelisted, [])

    def test_whitelisted_setter_empty(self):
        config = Configuration()
        config.whitelisted = ''
        self.assertEqual(config.whitelisted, [])

    def test_blacklisted_setter_list(self):
        config = Configuration()
        config.blacklisted = ['test']
        self.assertEqual(config.blacklisted, ['Test'])

    def test_blacklisted_setter_none(self):
        config = Configuration()
        config.blacklisted = None
        self.assertEqual(config.blacklisted, [])

    def test_blacklisted_setter_empty(self):
        config = Configuration()
        config.blacklisted = ''
        self.assertEqual(config.blacklisted, [])

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

    def test_ip_headers_setter_valid(self):
        config = Configuration()
        config.ip_headers = ['HTTP_X_FORWARDED_FOR']
        self.assertEqual(config.ip_headers, ['X-Forwarded-For'])

    def test_ip_headers_setter_invalid(self):
        config = Configuration()
        with self.assertRaises(ConfigurationError):
            config.ip_headers = 'invalid'

    def test_trusted_proxies_setter_valid(self):
        config = Configuration()
        config.trusted_proxies = ['2.2.2.2']
        self.assertEqual(config.trusted_proxies, ['2.2.2.2'])

    def test_trusted_proxies_setter_invalid(self):
        config = Configuration()
        with self.assertRaises(ConfigurationError):
            config.trusted_proxies = 'invalid'
