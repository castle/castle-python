from castle.test import unittest
from castle.logger import Logger
from castle.configuration import configuration


class TmpLogger(object):

    @staticmethod
    def info(message):
        return message


class LoggerTestCase(unittest.TestCase):

    def test_without_logger(self):
        configuration.logger = None
        self.assertEqual(Logger.call("Test"), None)

    def test_with_logger(self):
        configuration.logger = TmpLogger
        self.assertEqual(Logger.call("Test"), "[CASTLE] Test")
