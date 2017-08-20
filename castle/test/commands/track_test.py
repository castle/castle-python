from castle.test import unittest
from castle.command import Command
from castle.commands.track import CommandsTrack
from castle.context.merger import ContextMerger
from castle.exceptions import InvalidParametersError


class CommandsTrackTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(CommandsTrack({}).context_merger, ContextMerger)

    def test_build_no_event(self):
        with self.assertRaises(InvalidParametersError):
            CommandsTrack({}).build({})

    def test_build(self):
        options = {'event': '$login.authenticate', 'user_id': '1234', 'properties': {'test': '1'}, 'context': {'test': '1'}}
        command = CommandsTrack({}).build(options)
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'post')
        self.assertEqual(command.endpoint, 'track')
        self.assertEqual(command.data, {'name': '$login.authenticate', 'user_id': '1234', 'properties': {'test': '1'}, 'context': {'test': '1'}})

    def test_build_context(self):
        context = {'test': '1'}
        self.assertEqual(CommandsTrack({}).build_context(context), context)
