from castle.test import unittest
from castle.configuration import configuration
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
        configuration.whitelisted = []
        configuration.blacklisted = []

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

    def test_whitelisted_headers(self):
        configuration.whitelisted = ['Accept', 'OK']
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
#

    def test_restricted_blacklisted_headers(self):
        configuration.blacklisted = ['User-Agent']
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

    def test_blacklisted_headers(self):
        configuration.blacklisted = ['Accept']
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
#

    def test_blacklisted_and_whitelisted_headers(self):
        configuration.blacklisted = ['Accept']
        configuration.whitelisted = ['Accept']
        self.assertEqual(
            ExtractorsHeaders(formatted_headers()).call()['Accept'], True
        )
