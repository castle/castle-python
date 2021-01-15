from urllib.parse import urlparse
from castle.failover.strategy import FailoverStrategy
from castle.errors import ConfigurationError


def default_values(self, klass):
    config = klass()
    uri = urlparse('https://api.castle.io/v1')
    self.assertEqual(config.api_secret, None)
    self.assertEqual(config.base_url, uri)
    self.assertEqual(config.base_url.path, '/v1')
    self.assertEqual(config.allowlisted, [])
    self.assertEqual(config.denylisted, [])
    self.assertEqual(config.request_timeout, 1000)
    self.assertEqual(config.failover_strategy, FailoverStrategy.ALLOW.value)
    self.assertEqual(config.ip_headers, [])
    self.assertEqual(config.trusted_proxies, [])

def api_secret_setter(self, klass):
    config = klass()
    config.api_secret = 'test'
    self.assertEqual(config.api_secret, 'test')

def base_url_setter(self, klass):
    config = klass()
    config.base_url = 'test'
    self.assertEqual(config.base_url, urlparse('test'))

def base_url_setter_with_port(self, klass):
    config = klass()
    local_api_url = 'http://api.castle.local:3001/v1'
    config.base_url = local_api_url
    parsed_url = urlparse(local_api_url)
    self.assertEqual(config.base_url, parsed_url)
    self.assertEqual(config.base_url.path, '/v1')
    self.assertEqual(config.base_url.port, 3001)

def allowlisted_setter_list(self, klass):
    config = klass()
    config.allowlisted = ['test']
    self.assertEqual(config.allowlisted, ['Test'])

def allowlisted_setter_none(self, klass):
    config = klass()
    config.allowlisted = None
    self.assertEqual(config.allowlisted, [])

def allowlisted_setter_empty(self, klass):
    config = klass()
    config.allowlisted = ''
    self.assertEqual(config.allowlisted, [])

def denylisted_setter_list(self, klass):
    config = klass()
    config.denylisted = ['test']
    self.assertEqual(config.denylisted, ['Test'])

def denylisted_setter_none(self, klass):
    config = klass()
    config.denylisted = None
    self.assertEqual(config.denylisted, [])

def denylisted_setter_empty(self, klass):
    config = klass()
    config.denylisted = ''
    self.assertEqual(config.denylisted, [])

def request_timeout_setter(self, klass):
    config = klass()
    config.request_timeout = 5000
    self.assertEqual(config.request_timeout, 5000)

def failover_strategy_setter_valid(self, klass):
    config = klass()
    config.failover_strategy = FailoverStrategy.THROW.value
    self.assertEqual(config.failover_strategy, FailoverStrategy.THROW.value)

def failover_strategy_setter_invalid(self, klass):
    config = klass()
    with self.assertRaises(ConfigurationError):
        config.failover_strategy = 'invalid'

def ip_headers_setter_valid(self, klass):
    config = klass()
    config.ip_headers = ['HTTP_X_FORWARDED_FOR']
    self.assertEqual(config.ip_headers, ['X-Forwarded-For'])

def ip_headers_setter_invalid(self, klass):
    config = klass()
    with self.assertRaises(ConfigurationError):
        config.ip_headers = 'invalid'

def trusted_proxies_setter_valid(self, klass):
    config = klass()
    config.trusted_proxies = ['2.2.2.2']
    self.assertEqual(config.trusted_proxies, ['2.2.2.2'])

def trusted_proxies_setter_invalid(self, klass):
    config = klass()
    with self.assertRaises(ConfigurationError):
        config.trusted_proxies = 'invalid'
