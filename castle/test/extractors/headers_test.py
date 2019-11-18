from castle.test import unittest
from castle.configuration import configuration
from castle.extractors.headers import ExtractorsHeaders


def client_id():
    return 'abcd'


def environ():
    return {
        'HTTP_USER_AGENT': 'requests',
        'HTTP_OK': 'OK',
        'TEST': '1',
        'HTTP_COOKIE': "__cid={client_id};other=efgh".format(client_id=client_id)
    }


class ExtractorsHeadersTestCase(unittest.TestCase):
    def test_extract_headers(self):
        self.assertEqual(ExtractorsHeaders(environ()).call(),
                         {'Test': '1', 'User-Agent': 'requests'})

    def test_add_whitelisted_headers(self):
        configuration.whitelisted += ['TEST']
        self.assertEqual(
            ExtractorsHeaders(environ()).call(),
            {'User-Agent': 'requests', 'Test': '1'}
        )
        configuration.whitelisted.remove('Test')
