from castle.test import unittest
from castle.command import Command
from castle.commands.authenticate import CommandsAuthenticate
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsAuthenticateTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(CommandsAuthenticate({}).context_merger, ContextMerger)

    def test_build_no_event(self):
        with self.assertRaises(InvalidParametersError):
            CommandsAuthenticate({}).build({})

    def test_build_no_user_id(self):
        with self.assertRaises(InvalidParametersError):
            CommandsAuthenticate({}).build({'event': '$login.authenticate'})

    def test_build(self):
        options = {'event': '$login.authenticate', 'user_id': '1234', 'properties': {'test': '1'}, 'context': {'test': '1'}}
        command = CommandsAuthenticate({}).build(options)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'authenticate')
        self.assertEqual(command.data, {'properties': {'test': '1'}, 'context': {'test': '1'}, 'event': '$login.authenticate', 'user_id': '1234'})

    def test_build_context(self):
        context = {'test': '1'}
        self.assertEqual(CommandsAuthenticate({}).build_context(context), context)
