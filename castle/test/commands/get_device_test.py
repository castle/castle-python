from castle.test import unittest
from castle.command import Command
from castle.commands.get_device import CommandsGetDevice
from castle.errors import InvalidParametersError


def device_token():
    return '1234'


class CommandsGetDeviceTestCase(unittest.TestCase):
    def test_call_no_device_token(self):
        with self.assertRaises(InvalidParametersError):
            CommandsGetDevice.call('')

    def test_call(self):
        command = CommandsGetDevice.call(device_token())
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'get')
        self.assertEqual(command.path, 'devices/1234')
        self.assertEqual(command.data, None)
