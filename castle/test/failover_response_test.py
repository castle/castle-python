from castle.test import unittest
from castle.configuration import configuration
from castle.failover_response import FailoverResponse


def user_id():
    return '1234'


def strategy():
    return 'deny'


class FailoverResponseTestCase(unittest.TestCase):
    def test_strategy_passed(self):
        failover_response = FailoverResponse(user_id(), strategy())
        self.assertEqual(failover_response.user_id, user_id())
        self.assertEqual(failover_response.strategy, strategy())

    def test_strategy_not_passed(self):
        failover_response = FailoverResponse(user_id())
        self.assertEqual(failover_response.user_id, user_id())
        self.assertEqual(failover_response.strategy,
                         configuration.failover_strategy)

    def test_call(self):
        failover_response = FailoverResponse(user_id())
        self.assertDictEqual(
            failover_response.call(),
            {
                'action': configuration.failover_strategy,
                'user_id': user_id(),
                'failover': True,
                'failover_reason': None
            }
        )
