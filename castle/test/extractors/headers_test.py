from castle.test import unittest
from castle.configuration import configuration
from castle.extractors.headers import ExtractorsHeaders


def client_id():
    return 'abcd'


def environ():
    return {
        'HTTP_X_FORWARDED_FOR': '1.2.3.4',
        'HTTP_OK': 'OK',
        'TEST': '1',
        'HTTP_COOKIE': "__cid={client_id};other=efgh".format(client_id=client_id)
    }


class ExtractorsHeadersTestCase(unittest.TestCase):
    def test_extract_headers(self):
        self.assertEqual(ExtractorsHeaders(environ()).call(),
                         {'X-Forwarded-For': '1.2.3.4'})

    def test_extend_whitelisted_headers(self):
        configuration.whitelisted += ['TEST']
        self.assertEqual(
            ExtractorsHeaders(environ()).call(),
            {'X-Forwarded-For': '1.2.3.4', 'Test': '1'}
        )
        configuration.whitelisted.remove('Test')
