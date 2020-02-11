from castle.test import unittest, mock
from castle.extractors.ip import ExtractorsIp


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


class ExtractorsIpTestCase(unittest.TestCase):
    def test_extract_ip(self):
        self.assertEqual(ExtractorsIp(request()).call(), request_ip())

    def test_extract_ip_from_wsgi_request_remote_addr(self):
        self.assertEqual(
            ExtractorsIp(request_with_ip_remote_addr()).call(),
            request_ip()
        )
