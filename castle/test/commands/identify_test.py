from castle.test import mock, unittest
from castle.command import Command
from castle.commands.identify import CommandsIdentify
from castle.exceptions import InvalidParametersError
from castle.utils import clone


def default_options():
    """Default options include all required fields."""
    return {'user_id': '1234'}


def default_options_plus(**extra):
    """Default options plus the given extra fields."""
    options = default_options()
    options.update(extra)
    return options


def default_command_with_data(**data):
    """What we expect the identify command to look like."""
    return Command(
        method='post',
        path='identify',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )


class CommandsIdentifyTestCase(unittest.TestCase):
    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch('castle.commands.identify.timestamp')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = mock.sentinel.timestamp
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = mock.sentinel.test_init_context
        obj = CommandsIdentify(context)
        self.assertEqual(obj.context, context)

    def test_build(self):
        context = {'test': '1'}
        options = default_options_plus(context={'color': 'blue'})

        # expect the original context to have been merged with the context specified in the options
        expected_data = clone(options)
        expected_data.update(context={'test': '1', 'color': 'blue'})
        expected = default_command_with_data(**expected_data)

        self.assertEqual(CommandsIdentify(context).build(options), expected)

    def test_build_no_user_id(self):
        context = {}
        options = default_options()
        options.pop('user_id')

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsIdentify(context).build(options), expected)

    def test_build_properties_not_allowed(self):
        context = {'test': '1'}
        options = default_options_plus(properties={'hair': 'blonde'})

        with self.assertRaises(InvalidParametersError):
            CommandsIdentify(context).build(options)

    def test_build_user_traits_allowed(self):
        context = {}
        options = default_options_plus(user_traits={'email': 'identity@its.me.com'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsIdentify(context).build(options), expected)
