from castle.test import unittest
from castle.headers.format import HeadersFormat


class HeadersFormatTestCase(unittest.TestCase):
    def test_without_http(self):
        self.assertEqual(HeadersFormat.call('X_TEST'), 'X-Test')

    def test_call_removes_http_and_capitalizes(self):
        self.assertEqual(HeadersFormat.call('HTTP_X_TEST'), 'X-Test')

    def test_mixed_dividers(self):
        self.assertEqual(HeadersFormat.call('http-X_teST'), 'X-Test')

    def test_does_not_remove_http_if_there_is_no_divider(self):
        self.assertEqual(HeadersFormat.call('httpX_teST'), 'Httpx-Test')
