from castle.test import unittest
from castle.command import Command
from castle.commands.identify import CommandsIdentify
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsIdentifyTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(CommandsIdentify({}).context_merger, ContextMerger)

    def test_build_no_user_id(self):
        with self.assertRaises(InvalidParametersError):
            CommandsIdentify({}).build({})

    def test_build_active_true(self):
        options = {'user_id': '1234', 'active': True, 'traits': {'test': '1'}, 'context': {'test': '1'}}
        command = CommandsIdentify({}).build(options)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, {'active': True, 'traits': {'test': '1'}, 'context': {'test': '1'}, 'user_id': '1234'})

    def test_build_active_false(self):
        options = {'user_id': '1234', 'active': False}
        command = CommandsIdentify({}).build(options)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'identify')
        self.assertEqual(command.data, {'context': {}, 'user_id': '1234'})

    def test_build_context(self):
        context = {'test': '1'}
        self.assertEqual(CommandsIdentify({}).build_context(context), context)
