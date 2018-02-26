from castle.test import mock, unittest
from castle.command import Command
from castle.commands.impersonate import CommandsImpersonate
from castle.exceptions import InvalidParametersError
from castle.utils import clone


def default_options():
    """Default options include all required fields."""
    return {'impersonator': 'admin', 'user_id': '1234',
            'context': {'ip': '127.0.0.1', 'user_agent': 'Chrome'}}


def default_options_plus(**extra):
    """Default options plus the given extra fields."""
    options = default_options()
    options.update(extra)
    return options


def default_command_with_data(**data):
    """What we expect the impersonate command to look like."""
    return Command(
        method='post',
        path='impersonate',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )

def default_reset_command_with_data(**data):
    """What we expect the impersonate command to look like."""
    return Command(
        method='delete',
        path='impersonate',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )


class CommandsImpersonateTestCase(unittest.TestCase):
    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch('castle.commands.impersonate.timestamp')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = mock.sentinel.timestamp
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = mock.sentinel.test_init_context
        obj = CommandsImpersonate(context)
        self.assertEqual(obj.context, context)

    def test_build(self):
        context = {'lang': 'es'}
        options = default_options_plus(
            context={'local time': '8:53pm', 'ip': '127.0.0.1', 'user_agent': 'Chrome'}
        )

        # expect the original context to have been merged with the context specified in the options
        expected_data = clone(options)
        expected_data.update(
            context={'lang': 'es', 'local time': '8:53pm',
                     'ip': '127.0.0.1', 'user_agent': 'Chrome'}
        )
        expected = default_command_with_data(**expected_data)

        self.assertEqual(CommandsImpersonate(context).build(options), expected)

    def test_reset_build(self):
        context = {'lang': 'es'}
        options = default_options_plus(
            reset=True,
            context={'lang': 'es', 'local time': '8:53pm',
                     'ip': '127.0.0.1', 'user_agent': 'Chrome'}
        )

        # expect the original context to have been merged with the context specified in the options
        expected_data = clone(options)
        expected_data.update(
            context={'lang': 'es', 'local time': '8:53pm',
                     'ip': '127.0.0.1', 'user_agent': 'Chrome'}
        )
        expected = default_reset_command_with_data(**expected_data)

        self.assertEqual(CommandsImpersonate(context).build(options), expected)

    def test_build_no_event(self):
        context = {}
        options = default_options()
        options.pop('user_id')

        with self.assertRaises(InvalidParametersError):
            CommandsImpersonate(context).build(options)

    def test_build_no_context_ip(self):
        context = {}
        options = default_options()
        options['context'].pop('ip')

        with self.assertRaises(InvalidParametersError):
            CommandsImpersonate(context).build(options)

    def test_build_no_context_user_agent(self):
        context = {}
        options = default_options()
        options['context'].pop('user_agent')

        with self.assertRaises(InvalidParametersError):
            CommandsImpersonate(context).build(options)
