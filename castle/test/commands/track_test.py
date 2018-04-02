from castle.test import mock, unittest
from castle.command import Command
from castle.commands.track import CommandsTrack
from castle.exceptions import InvalidParametersError
from castle.utils import clone


def default_options():
    """Default options include all required fields."""
    return {'event': '$login.authenticate'}


def default_options_plus(**extra):
    """Default options plus the given extra fields."""
    options = default_options()
    options.update(extra)
    return options


def default_command_with_data(**data):
    """What we expect the authenticate command to look like."""
    return Command(
        method='post',
        path='track',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )


class CommandsTrackTestCase(unittest.TestCase):
    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch('castle.commands.track.timestamp')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = mock.sentinel.timestamp
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = mock.sentinel.test_init_context
        obj = CommandsTrack(context)
        self.assertEqual(obj.context, context)

    def test_build(self):
        context = {'lang': 'es'}
        options = default_options_plus(context={'local time': '8:53pm'})

        # expect the original context to have been merged with the context specified in the options
        expected_data = clone(options)
        expected_data.update(context={'lang': 'es', 'local time': '8:53pm'})
        expected = default_command_with_data(**expected_data)

        self.assertEqual(CommandsTrack(context).build(options), expected)

    def test_build_no_event(self):
        context = {}
        options = default_options()
        options.pop('event')

        with self.assertRaises(InvalidParametersError):
            CommandsTrack(context).build(options)

    def test_build_properties_allowed(self):
        context = {}
        options = default_options_plus(properties={'face': 'handsome'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsTrack(context).build(options), expected)

    def test_build_user_traits_allowed(self):
        context = {}
        options = default_options_plus(
            user_traits={'email': 'track@all.the.things.com'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsTrack(context).build(options), expected)
