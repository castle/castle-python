from castle.test import unittest
from castle.command import Command
from castle.commands.report_device import CommandsReportDevice


def device_token():
    return '1234'


class CommandsReportDeviceTestCase(unittest.TestCase):
    def test_call(self):
        command = CommandsReportDevice.call(device_token())
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'put')
        self.assertEqual(command.path, 'devices/1234/report')
        self.assertEqual(command.data, None)
