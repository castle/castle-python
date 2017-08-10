from castle.test import unittest
from castle.configuration import configuration
from castle.failover_response import FailoverResponse


class FailoverResponseTestCase(unittest.TestCase):
    def user_id(self):
        return '1234'

    def strategy(self):
        return 'deny'

    def test_strategy_passed(self):
        failover_response = FailoverResponse(self.user_id(), self.strategy())
        self.assertEqual(failover_response.user_id, self.user_id())
        self.assertEqual(failover_response.strategy, self.strategy())

    def test_strategy_not_passed(self):
        failover_response = FailoverResponse(self.user_id())
        self.assertEqual(failover_response.user_id, self.user_id())
        self.assertEqual(failover_response.strategy, configuration.failover_strategy)

    def test_call(self):
        failover_response = FailoverResponse(self.user_id())
        self.assertDictEqual(failover_response.call(), {'action': configuration.failover_strategy, 'user_id': self.user_id()})
