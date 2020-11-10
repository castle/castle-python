from castle.test import unittest
from castle.verdict import Verdict


class VerdictTestCase(unittest.TestCase):
    def test_allow(self):
        self.assertEqual(Verdict.ALLOW.value, 'allow')

    def test_challenge(self):
        self.assertEqual(Verdict.CHALLENGE.value, 'challenge')

    def test_deny(self):
        self.assertEqual(Verdict.DENY.value, 'deny')
