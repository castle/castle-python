from castle.test import unittest, mock
from castle.configuration import configuration
from castle.extractors.ip import ExtractorsIp


class ExtractorsIpTestCase(unittest.TestCase):
    def request_ip(self):
        return '127.0.0.1'

    def request(self):
        r = mock.Mock(spec=['ip'])
        r.ip = self.request_ip()
        return r

    def request_without_ip_remote_addr(self):
        r = mock.Mock(spec=['environ'])
        r.environ = {'REMOTE_ADDR': self.request_ip()}
        return r

    def request_without_ip_x_forwarded_for(self):
        r = mock.Mock(spec=['environ'])
        r.environ = {'HTTP_X_FORWARDED_FOR': self.request_ip()}
        return r

    def test_extract_ip(self):
        self.assertEqual(ExtractorsIp(self.request()).call(), self.request_ip())

    def test_extract_ip_from_wsgi_request_remote_addr(self):
        self.assertEqual(ExtractorsIp(self.request_without_ip_remote_addr()).call(), self.request_ip())

    def test_extract_ip_from_wsgi_request_x_forwarded_for(self):
        self.assertEqual(ExtractorsIp(self.request_without_ip_x_forwarded_for()).call(), self.request_ip())
