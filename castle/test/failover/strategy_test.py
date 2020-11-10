from castle.test import unittest
from castle.failover.strategy import FailoverStrategy


class FailoverStrategyTestCase(unittest.TestCase):
    def test_allow(self):
        self.assertEqual(FailoverStrategy.ALLOW.value, 'allow')

    def test_challenge(self):
        self.assertEqual(FailoverStrategy.CHALLENGE.value, 'challenge')

    def test_deny(self):
        self.assertEqual(FailoverStrategy.DENY.value, 'deny')

    def test_throw(self):
        self.assertEqual(FailoverStrategy.THROW.value, 'throw')

    def test_list(self):
        self.assertEqual(FailoverStrategy.list(), ['allow', 'challenge', 'deny', 'throw'])
