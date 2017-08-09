import unittest
import pdb
from castle.configuration import configuration
from castle.extractors.headers import ExtractorsHeaders


class ExtractorsHeadersTestCase(unittest.TestCase):
    def client_id(self):
        return 'abcd'

    def environ(self):
        return {
            'HTTP_X_FORWARDED_FOR': '1.2.3.4',
            'HTTP_OK': 'OK',
            'TEST': '1',
            'HTTP_COOKIE': "__cid={self.client_id()};other=efgh"
        }

    def test_extract_headers(self):
        self.assertEqual(ExtractorsHeaders(self.environ()).call(), { 'X-Forwarded-For': '1.2.3.4' })

    def test_extend_whitelisted_headers(self):
        configuration.whitelisted += ['TEST']
        self.assertEqual(ExtractorsHeaders(self.environ()).call(), { 'X-Forwarded-For': '1.2.3.4', 'Test': '1' })
        configuration.whitelisted.remove('Test')
