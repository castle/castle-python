from castle.test import unittest
from castle.command import Command
from castle.commands.approve_device import CommandsApproveDevice


def device_token():
    return '1234'


class CommandsApproveDeviceTestCase(unittest.TestCase):
    def test_call(self):
        command = CommandsApproveDevice.call(device_token())
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'put')
        self.assertEqual(command.path, 'devices/1234/approve')
        self.assertEqual(command.data, None)
