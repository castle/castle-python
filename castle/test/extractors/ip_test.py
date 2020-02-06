from castle.test import unittest, mock
from castle.extractors.ip import ExtractorsIp
from castle.configuration import configuration


def request_ip():
    return '127.0.0.1'


def request_ip_next():
    return '127.0.0.2'


def request():
    req = mock.Mock(spec=['ip'])
    req.ip = request_ip()
    return req


def request_with_ip_remote_addr():
    req = mock.Mock(spec=['environ'])
    req.environ = {'REMOTE_ADDR': request_ip()}
    return req


def request_with_ip_x_forwarded_for():
    req = mock.Mock(spec=['environ'])
    req.environ = {'HTTP_X_FORWARDED_FOR': request_ip()}
    return req


def request_with_ip_cf_connecting_ip():
    req = mock.Mock(spec=['environ'])
    req.environ = {'HTTP_CF_CONNECTING_IP': request_ip_next()}
    return req


class ExtractorsIpTestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        configuration.ip_headers = []

    def test_extract_ip(self):
        self.assertEqual(ExtractorsIp(request()).call(), request_ip())

    def test_extract_ip_from_wsgi_request_remote_addr(self):
        self.assertEqual(
            ExtractorsIp(request_with_ip_remote_addr()).call(),
            request_ip()
        )

    def test_extract_ip_from_wsgi_request_configured_ip_header_first(self):
        configuration.ip_headers = ["HTTP_CF_CONNECTING_IP"]
        self.assertEqual(
            ExtractorsIp(request_with_ip_cf_connecting_ip()).call(),
            request_ip_next()
        )
        configuration.ip_headers = []

    def test_extract_ip_from_wsgi_request_configured_ip_header_second(self):
        configuration.ip_headers = ["HTTP_CF_CONNECTING_IP", "HTTP_X_FORWARDED_FOR"]
        self.assertEqual(
            ExtractorsIp(request_with_ip_x_forwarded_for()).call(),
            request_ip()
        )
        configuration.ip_headers = []
