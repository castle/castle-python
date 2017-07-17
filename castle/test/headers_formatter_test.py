from castle.test import unittest
from castle.headers_formatter import HeadersFormatter


class HeadersFormatterTestCase(unittest.TestCase):
    def test_without_http(self):
        self.assertEqual(HeadersFormatter.call('X_TEST'), 'X-Test')

    def test_call_removes_http_and_capitalizes(self):
        self.assertEqual(HeadersFormatter.call('HTTP_X_TEST'), 'X-Test')

    def test_mixed_dividers(self):
        self.assertEqual(HeadersFormatter.call('http-X_teST'), 'X-Test')

    def test_does_not_remove_http_if_there_is_no_divider(self):
        self.assertEqual(HeadersFormatter.call('httpX_teST'), 'Httpx-Test')
