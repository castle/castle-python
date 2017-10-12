from castle.test import unittest
from castle.command import Command
from castle.commands.track import CommandsTrack
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


def default_payload():
    return {'event': '$login.authenticate'}

class CommandsTrackTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(CommandsTrack({}).context_merger, ContextMerger)

    def test_build(self):
        payload = default_payload()
        payload.update(context={'test': '1'})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, payload)

    def test_build_user_id(self):
        payload = default_payload()
        payload.update(user_id='1234')
        command_data = default_payload()
        command_data.update(user_id='1234', context={})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, command_data)

    def test_build_properties(self):
        payload = default_payload()
        payload.update(properties={'test': '1'})
        command_data = default_payload()
        command_data.update(properties={'test': '1'}, context={})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, command_data)

    def test_build_traits(self):
        payload = default_payload()
        payload.update(traits={'test': '1'})
        command_data = default_payload()
        command_data.update(traits={'test': '1'}, context={})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, command_data)

    def test_build_active_true(self):
        payload = default_payload()
        payload.update(context={'active': True})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, payload)

    def test_build_active_false(self):
        payload = default_payload()
        payload.update(context={'active': False})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, payload)

    def test_build_active_string(self):
        payload = default_payload()
        payload.update(context={'active': 'string'})
        command_data = default_payload()
        command_data.update(context={})
        command = CommandsTrack({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, command_data)

    def test_validate_no_event(self):
        with self.assertRaises(InvalidParametersError):
            CommandsTrack({}).validate({'user_id': '1234'})

    def test_build_context(self):
        context = {'test': '1'}
        self.assertEqual(CommandsTrack({}).build_context(context), context)
