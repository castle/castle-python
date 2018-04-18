from castle.test import unittest

from castle.extractors.client_id import ExtractorsClientId


def client_id():
    return 'cookies'


def client_id_environ():
    return 'environ'


def cookies():
    return {'__cid': client_id()}


def environ():
    return {'HTTP_X_CASTLE_CLIENT_ID': client_id_environ()}


class ExtractorsClientIdTestCase(unittest.TestCase):
    def test_extract_client_id_from_cookiesand_environ(self):
        self.assertEqual(
            ExtractorsClientId(environ(), cookies()).call(),
            client_id_environ()
        )

    def test_extract_client_id_from_cookies(self):
        self.assertEqual(
            ExtractorsClientId({}, cookies()).call(),
            client_id()
        )

    def test_extract_client_id_from_environ(self):
        self.assertEqual(ExtractorsClientId(
            environ(), {}).call(), client_id_environ())

    def test_extract_client_id_unavailable(self):
        self.assertEqual(ExtractorsClientId({}, {}).call(), '')

    def test_extract_client_id_no_cookies(self):
        self.assertEqual(ExtractorsClientId({}).call(), '')
