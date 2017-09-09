from castle.test import unittest
from castle.command import Command
from castle.commands.identify import CommandsIdentify
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


def default_payload():
    return {'user_id': '1234'}

class CommandsIdentifyTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(CommandsIdentify({}).context_merger, ContextMerger)

    def test_build_no_user_id(self):
        with self.assertRaises(InvalidParametersError):
            CommandsIdentify({}).build({})

    def test_build(self):
        payload = default_payload()
        payload.update(context={'test': '1'})
        command = CommandsIdentify({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, payload)

    def test_build_traits(self):
        payload = default_payload()
        payload.update(traits={'test': '1'})
        command_data = default_payload()
        command_data.update(traits={'test': '1'}, context={})
        command = CommandsIdentify({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, command_data)

    def test_build_active_true(self):
        payload = default_payload()
        payload.update(context={'active': True})
        command = CommandsIdentify({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, payload)

    def test_build_active_false(self):
        payload = default_payload()
        payload.update(context={'active': False})
        command = CommandsIdentify({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, payload)

    def test_build_active_string(self):
        payload = default_payload()
        payload.update(context={'active': 'string'})
        command_data = default_payload()
        command_data.update(context={})
        command = CommandsIdentify({}).build(payload)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, command_data)


    def test_build_context(self):
        context = {'test': '1'}
        self.assertEqual(CommandsIdentify({}).build_context(context), context)
