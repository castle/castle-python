from castle.test import unittest
from castle.configuration import configuration, DEFAULT_ALLOWLIST
from castle.extractors.headers import ExtractorsHeaders


def formatted_headers():
    return dict({
        'Content-Length': '0',
        'Authorization': 'Basic 123456',
        'Cookie': '__cid=abcd;other=efgh',
        'Ok': 'OK',
        'Accept': 'application/json',
        'X-Forwarded-For': '1.2.3.4',
        'User-Agent': 'Mozilla 1234'
    })


class ExtractorsHeadersTestCase(unittest.TestCase):

    def tearDown(self):
        configuration.allowlisted = []
        configuration.denylisted = []

    def test_extract_headers(self):
        self.assertEqual(ExtractorsHeaders(formatted_headers()).call(),
                         {'Accept': 'application/json',
                          'Authorization': True,
                          'Cookie': True,
                          'Content-Length': '0',
                          'Ok': 'OK',
                          'User-Agent': 'Mozilla 1234',
                          'X-Forwarded-For': '1.2.3.4'
                          })

    def test_allowlisted_headers(self):
        configuration.allowlisted = ['Accept', 'OK']
        self.assertEqual(
            ExtractorsHeaders(formatted_headers()).call(),
            {'Accept': 'application/json',
             'Authorization': True,
             'Cookie': True,
             'Content-Length': True,
             'Ok': 'OK',
             'User-Agent': 'Mozilla 1234',
             'X-Forwarded-For': True
             }
        )

    def test_only_default_allowlisted_headers(self):
        configuration.allowlisted = DEFAULT_ALLOWLIST
        self.assertEqual(
            ExtractorsHeaders(formatted_headers()).call(),
            {'Accept': 'application/json',
             'Authorization': True,
             'Cookie': True,
             'Ok': True,
             'Content-Length': '0',
             'User-Agent': 'Mozilla 1234',
             'X-Forwarded-For': True
             }
        )

    def test_restricted_denylisted_headers(self):
        configuration.denylisted = ['User-Agent']
        self.assertEqual(
            ExtractorsHeaders(formatted_headers()).call(),
            {'Accept': 'application/json',
             'Authorization': True,
             'Cookie': True,
             'Content-Length': '0',
             'Ok': 'OK',
             'User-Agent': 'Mozilla 1234',
             'X-Forwarded-For': '1.2.3.4'
             }
        )

    def test_denylisted_headers(self):
        configuration.denylisted = ['Accept']
        self.assertEqual(
            ExtractorsHeaders(formatted_headers()).call(),
            {'Accept': True,
             'Authorization': True,
             'Cookie': True,
             'Content-Length': '0',
             'Ok': 'OK',
             'User-Agent': 'Mozilla 1234',
             'X-Forwarded-For': '1.2.3.4'
             }
        )

    def test_denylisted_and_allowlisted_headers(self):
        configuration.denylisted = ['Accept']
        configuration.allowlisted = ['Accept']
        self.assertEqual(
            ExtractorsHeaders(formatted_headers()).call()['Accept'], True
        )
