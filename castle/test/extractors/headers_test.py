from castle.test import unittest
from castle.configuration import configuration, WHITE_LIST
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
        configuration.white_list = []
        self.assertEqual(ExtractorsHeaders(environ()).call(),
                         {'User-Agent': 'requests', 'Ok': 'OK', 'Test': '1', 'Cookie': True})

    def test_add_white_list_headers(self):
        configuration.white_list = WHITE_LIST + ['TEST']
        self.assertEqual(
            ExtractorsHeaders(environ()).call(),
            {'User-Agent': 'requests', 'Test': '1', 'Cookie': True, 'Ok': True}
        )
        configuration.white_list = []
