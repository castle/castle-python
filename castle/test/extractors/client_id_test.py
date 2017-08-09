import unittest

from castle.configuration import configuration
from castle.extractors.client_id import ExtractorsClientId


class ExtractorsClientIdTestCase(unittest.TestCase):
    def client_id(self):
        return 'cookies'

    def client_id_environ(self):
        return 'environ'

    def cookies(self):
        return { '__cid': self.client_id() }

    def environ(self):
        return {
            'HTTP_X_CASTLE_CLIENT_ID': self.client_id_environ()
        }

    def test_extract_client_id_from_cookies(self):
        self.assertEqual(ExtractorsClientId(self.environ(), self.cookies()).call(), self.client_id())

    def test_extract_client_id_from_environ(self):
        self.assertEqual(ExtractorsClientId(self.environ(), {}).call(), self.client_id_environ())

    def test_extract_client_id_unavailable(self):
        self.assertEqual(ExtractorsClientId({}, {}).call(), '')
