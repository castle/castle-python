from castle.test import unittest
from castle.configuration import Configuration, SingletonConfiguration
from castle.test.helpers.configuration_helper import default_values, api_secret_setter, \
    base_url_setter, base_url_setter_with_port, allowlisted_setter_list, allowlisted_setter_none, \
    allowlisted_setter_empty, denylisted_setter_list, denylisted_setter_none, \
    denylisted_setter_empty, request_timeout_setter, failover_strategy_setter_valid, \
    failover_strategy_setter_invalid, ip_headers_setter_valid, ip_headers_setter_invalid, \
    trusted_proxies_setter_valid, trusted_proxies_setter_invalid


class ConfigurationTestCase(unittest.TestCase):
    def test_default_values(self):
        default_values(self, Configuration)

    def test_api_secret_setter(self):
        api_secret_setter(self, Configuration)

    def test_base_url_setter(self):
        base_url_setter(self, Configuration)

    def test_base_url_setter_with_port(self):
        base_url_setter_with_port(self, Configuration)

    def test_allowlisted_setter_list(self):
        allowlisted_setter_list(self, Configuration)

    def test_allowlisted_setter_none(self):
        allowlisted_setter_none(self, Configuration)

    def test_allowlisted_setter_empty(self):
        allowlisted_setter_empty(self, Configuration)

    def test_denylisted_setter_list(self):
        denylisted_setter_list(self, Configuration)

    def test_denylisted_setter_none(self):
        denylisted_setter_none(self, Configuration)

    def test_denylisted_setter_empty(self):
        denylisted_setter_empty(self, Configuration)

    def test_request_timeout_setter(self):
        request_timeout_setter(self, Configuration)

    def test_failover_strategy_setter_valid(self):
        failover_strategy_setter_valid(self, Configuration)

    def test_failover_strategy_setter_invalid(self):
        failover_strategy_setter_invalid(self, Configuration)

    def test_ip_headers_setter_valid(self):
        ip_headers_setter_valid(self, Configuration)

    def test_ip_headers_setter_invalid(self):
        ip_headers_setter_invalid(self, Configuration)

    def test_trusted_proxies_setter_valid(self):
        trusted_proxies_setter_valid(self, Configuration)

    def test_trusted_proxies_setter_invalid(self):
        trusted_proxies_setter_invalid(self, Configuration)


class SingletonConfigurationTestCase(unittest.TestCase):
    def test_default_values(self):
        default_values(self, SingletonConfiguration)

    def test_api_secret_setter(self):
        api_secret_setter(self, SingletonConfiguration)

    def test_base_url_setter(self):
        base_url_setter(self, SingletonConfiguration)

    def test_base_url_setter_with_port(self):
        base_url_setter_with_port(self, SingletonConfiguration)

    def test_allowlisted_setter_list(self):
        allowlisted_setter_list(self, SingletonConfiguration)

    def test_allowlisted_setter_none(self):
        allowlisted_setter_none(self, SingletonConfiguration)

    def test_allowlisted_setter_empty(self):
        allowlisted_setter_empty(self, SingletonConfiguration)

    def test_denylisted_setter_list(self):
        denylisted_setter_list(self, SingletonConfiguration)

    def test_denylisted_setter_none(self):
        denylisted_setter_none(self, SingletonConfiguration)

    def test_denylisted_setter_empty(self):
        denylisted_setter_empty(self, SingletonConfiguration)

    def test_request_timeout_setter(self):
        request_timeout_setter(self, SingletonConfiguration)

    def test_failover_strategy_setter_valid(self):
        failover_strategy_setter_valid(self, SingletonConfiguration)

    def test_failover_strategy_setter_invalid(self):
        failover_strategy_setter_invalid(self, SingletonConfiguration)

    def test_ip_headers_setter_valid(self):
        ip_headers_setter_valid(self, SingletonConfiguration)

    def test_ip_headers_setter_invalid(self):
        ip_headers_setter_invalid(self, SingletonConfiguration)

    def test_trusted_proxies_setter_valid(self):
        trusted_proxies_setter_valid(self, SingletonConfiguration)

    def test_trusted_proxies_setter_invalid(self):
        trusted_proxies_setter_invalid(self, SingletonConfiguration)
