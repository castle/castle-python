from castle.test import unittest

from castle.fingerprint.extract import FingerprintExtract


def fingerprint():
    return 'cookies'


def fingerprint_environ():
    return 'environ'


def cookies():
    return {'__cid': fingerprint()}


def environ():
    return {'X-Castle-Client-Id': fingerprint_environ()}


class FingerprintExtractTestCase(unittest.TestCase):
    def test_extract_fingerprint_from_cookiesand_environ(self):
        self.assertEqual(
            FingerprintExtract(environ(), cookies()).call(),
            fingerprint_environ()
        )

    def test_extract_fingerprint_from_cookies(self):
        self.assertEqual(
            FingerprintExtract({}, cookies()).call(),
            fingerprint()
        )

    def test_extract_fingerprint_from_environ(self):
        self.assertEqual(FingerprintExtract(
            environ(), {}).call(), fingerprint_environ())

    def test_extract_fingerprint_unavailable(self):
        self.assertEqual(FingerprintExtract({}, {}).call(), '')

    def test_extract_fingerprint_no_cookies(self):
        self.assertEqual(FingerprintExtract({}).call(), '')
