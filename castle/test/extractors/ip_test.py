from castle.test import unittest, mock
from castle.configuration import configuration
from castle.extractors.ip import ExtractorsIp


class ExtractorsIpTestCase(unittest.TestCase):
    def request_ip(self):
        return '127.0.0.1'

    def request(self):
        r = mock.Mock()
        r.ip = self.request_ip()
        return r

    def test_extract_ip(self):
        self.assertEqual(ExtractorsIp(self.request()).call(), self.request_ip())
