from castle.test import unittest
from castle.command import Command
from castle.commands.get_devices_for_user import CommandsGetDevicesForUser
from castle.errors import InvalidParametersError


def user_id():
    return '1234'


class CommandsGetDevicesForUserTestCase(unittest.TestCase):
    def test_build_no_user_id(self):
        with self.assertRaises(InvalidParametersError):
            CommandsGetDevicesForUser.build('')

    def test_build(self):
        command = CommandsGetDevicesForUser.build(user_id())
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'get')
        self.assertEqual(command.path, 'users/1234/devices')
        self.assertEqual(command.data, None)
