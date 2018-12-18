from castle.test import mock, unittest
from castle.command import Command
from castle.commands.authenticate import CommandsAuthenticate
from castle.exceptions import InvalidParametersError
from castle.utils import clone


def default_options():
    """Default options include all required fields."""
    return {'event': '$login.authenticate', 'user_id': '1234'}


def default_options_plus(**extra):
    """Default options plus the given extra fields."""
    options = default_options()
    options.update(extra)
    return options


def default_command_with_data(**data):
    """What we expect the authenticate command to look like."""
    return Command(
        method='post',
        path='authenticate',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )


class CommandsAuthenticateTestCase(unittest.TestCase):

    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch(
            'castle.commands.authenticate.timestamp')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = mock.sentinel.timestamp
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = mock.sentinel.test_init_context
        obj = CommandsAuthenticate(context)
        self.assertEqual(obj.context, context)

    def test_build(self):
        context = {'test': '1'}
        options = default_options_plus(context={'spam': True})

        # expect the original context to have been merged with the context specified in the options
        expected_data = clone(options)
        expected_data.update(context={'test': '1', 'spam': True})
        expected = default_command_with_data(**expected_data)

        self.assertEqual(CommandsAuthenticate(
            context).build(options), expected)

    def test_build_no_event(self):
        context = {}
        options = default_options()
        options.pop('event')

        with self.assertRaises(InvalidParametersError):
            CommandsAuthenticate(context).build(options)

    def test_build_no_user_id(self):
        context = {}
        options = default_options()
        options.pop('user_id')

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsAuthenticate(context).build(options), expected)

    def test_build_properties_allowed(self):
        context = {}
        options = default_options_plus(properties={'test': '1'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsAuthenticate(
            context).build(options), expected)

    def test_build_user_traits_allowed(self):
        context = {}
        options = default_options_plus(user_traits={'email': 'a@b.com'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsAuthenticate(
            context).build(options), expected)
