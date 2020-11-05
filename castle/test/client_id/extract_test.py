from castle.test import unittest

from castle.client_id.extract import ClientIdExtract


def client_id():
    return 'cookies'


def client_id_environ():
    return 'environ'


def cookies():
    return {'__cid': client_id()}


def environ():
    return {'X-Castle-Client-Id': client_id_environ()}


class ClientIdExtractTestCase(unittest.TestCase):
    def test_extract_client_id_from_cookiesand_environ(self):
        self.assertEqual(
            ClientIdExtract(environ(), cookies()).call(),
            client_id_environ()
        )

    def test_extract_client_id_from_cookies(self):
        self.assertEqual(
            ClientIdExtract({}, cookies()).call(),
            client_id()
        )

    def test_extract_client_id_from_environ(self):
        self.assertEqual(ClientIdExtract(
            environ(), {}).call(), client_id_environ())

    def test_extract_client_id_unavailable(self):
        self.assertEqual(ClientIdExtract({}, {}).call(), '')

    def test_extract_client_id_no_cookies(self):
        self.assertEqual(ClientIdExtract({}).call(), '')
