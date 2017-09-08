from castle.test import unittest
from castle.command import Command
from castle.commands.authenticate import CommandsAuthenticate
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


def default_payload():
    return {'event': '$login.authenticate', 'user_id': '1234'}

class CommandsAuthenticateTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(CommandsAuthenticate({}).context_merger, ContextMerger)

    def test_build_no_event(self):
        payload = {'user_id': '1234'}

        with self.assertRaises(InvalidParametersError):
            CommandsAuthenticate({}).build(payload)

    def test_build_no_user_id(self):
        payload = {'event': '$login.authenticate'}

        with self.assertRaises(InvalidParametersError):
            CommandsAuthenticate({}).build(payload)

    def test_build(self):
        payload = default_payload()
        payload.update(context={'test': '1'})
        command = CommandsAuthenticate({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, payload)

    def test_build_properties(self):
        payload = default_payload()
        payload.update(properties={'test': '1'})
        command_data = default_payload()
        command_data.update(properties={'test': '1'}, context={})
        command = CommandsAuthenticate({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, command_data)

    def test_build_traits(self):
        payload = default_payload()
        payload.update(traits={'test': '1'})
        command_data = default_payload()
        command_data.update(traits={'test': '1'}, context={})
        command = CommandsAuthenticate({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, command_data)

    def test_build_active_true(self):
        payload = default_payload()
        payload.update(context={'active': True})
        command = CommandsAuthenticate({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, payload)

    def test_build_active_false(self):
        payload = default_payload()
        payload.update(context={'active': False})
        command = CommandsAuthenticate({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, payload)

    def test_build_active_string(self):
        payload = default_payload()
        payload.update(context={'active': 'string'})
        command_data = default_payload()
        command_data.update(context={'active': True})
        command = CommandsAuthenticate({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, command_data)

    def test_build_context(self):
        context = {'test': '1'}
        self.assertEqual(CommandsAuthenticate({}).build_context(context), context)
