from castle.test import unittest
from castle.command import Command
from castle.commands.report_device import CommandsReportDevice
from castle.errors import InvalidParametersError


def device_token():
    return '1234'


class CommandsReportDeviceTestCase(unittest.TestCase):
    def test_build_no_device_token(self):
        with self.assertRaises(InvalidParametersError):
            CommandsReportDevice.build('')

    def test_build(self):
        command = CommandsReportDevice.build(device_token())
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'put')
        self.assertEqual(command.path, 'devices/1234/report')
        self.assertEqual(command.data, None)
