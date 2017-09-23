from castle.test import unittest, mock
from castle.extractors.ip import ExtractorsIp


def request_ip():
    return '127.0.0.1'

def request():
    req = mock.Mock(spec=['ip'])
    req.ip = request_ip()
    return req

def request_without_ip_remote_addr():
    req = mock.Mock(spec=['environ'])
    req.environ = {'REMOTE_ADDR': request_ip()}
    return req

def request_without_ip_x_forwarded_for():
    req = mock.Mock(spec=['environ'])
    req.environ = {'HTTP_X_FORWARDED_FOR': request_ip()}
    return req

class ExtractorsIpTestCase(unittest.TestCase):
    def test_extract_ip(self):
        self.assertEqual(ExtractorsIp(request()).call(), request_ip())

    def test_extract_ip_from_wsgi_request_remote_addr(self):
        self.assertEqual(
            ExtractorsIp(request_without_ip_remote_addr()).call(),
            request_ip()
        )

    def test_extract_ip_from_wsgi_request_x_forwarded_for(self):
        self.assertEqual(
            ExtractorsIp(request_without_ip_x_forwarded_for()).call(),
            request_ip()
        )
