from castle.test import mock, unittest
from castle.command import Command
from castle.commands.filter import CommandsFilter
from castle.utils.clone import UtilsClone


def default_options():
    """Default options include all required fields."""
    return {
        'request_token': '7e51335b-f4bc-4bc7-875d-b713fb61eb23-bf021a3022a1a302',
        'event': '$registration',
        'status': '',
        'user': {
            'id': '1234'
        }
    }


def default_options_plus(**extra):
    """Default options plus the given extra fields."""
    options = default_options()
    options.update(extra)
    return options


def default_command_with_data(**data):
    """What we expect the filter command to look like."""
    return Command(
        method='post',
        path='filter',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )


class CommandsFilterTestCase(unittest.TestCase):

    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch(
            'castle.commands.filter.generate_timestamp.call')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = mock.sentinel.timestamp
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = mock.sentinel.test_init_context
        obj = CommandsFilter(context)
        self.assertEqual(obj.context, context)

    def test_call(self):
        context = {'test': '1'}
        options = default_options_plus(context={'spam': True})

        # expect the original context to have been merged with the context specified in the options
        expected_data = UtilsClone.call(options)
        expected_data.update(context={'test': '1', 'spam': True})
        expected = default_command_with_data(**expected_data)

        self.assertEqual(CommandsFilter(
            context).call(options), expected)

    def test_call_properties_allowed(self):
        context = {}
        options = default_options_plus(properties={'test': '1'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsFilter(
            context).call(options), expected)

    def test_call_user_traits_allowed(self):
        context = {}
        options = default_options_plus(user_traits={'email': 'a@b.com'})
        options.update({'context': context})

        expected = default_command_with_data(**options)

        self.assertEqual(CommandsFilter(
            context).call(options), expected)
