from castle.test import mock, unittest
from castle.command import Command
from castle.commands.end_impersonation import CommandsEndImpersonation
from castle.errors import InvalidParametersError
from castle.utils.clone import UtilsClone


def default_options():
    """Default options include all required fields."""
    return {'properties': {'impersonator': 'admin'}, 'user_id': '1234',
            'context': {'ip': '127.0.0.1', 'user_agent': 'Chrome'}}


def default_options_plus(**extra):
    """Default options plus the given extra fields."""
    options = default_options()
    options.update(extra)
    return options


def default_command_with_data(**data):
    """What we expect the impersonate command to look like."""
    return Command(
        method='delete',
        path='impersonate',
        data=dict(sent_at=mock.sentinel.timestamp, **data)
    )


class CommandsEndImpersonationTestCase(unittest.TestCase):
    def setUp(self):
        # patch timestamp to return a known value
        timestamp_patcher = mock.patch(
            'castle.commands.end_impersonation.generate_timestamp.call')
        self.mock_timestamp = timestamp_patcher.start()
        self.mock_timestamp.return_value = mock.sentinel.timestamp
        self.addCleanup(timestamp_patcher.stop)

    def test_init(self):
        context = mock.sentinel.test_init_context
        obj = CommandsEndImpersonation(context)
        self.assertEqual(obj.context, context)

    def test_call(self):
        context = {'lang': 'es'}
        options = default_options_plus(
            context={'local time': '8:53pm', 'ip': '127.0.0.1', 'user_agent': 'Chrome'}
        )

        # expect the original context to have been merged with the context specified in the options
        expected_data = UtilsClone.call(options)
        expected_data.update(
            context={'lang': 'es', 'local time': '8:53pm',
                     'ip': '127.0.0.1', 'user_agent': 'Chrome'}
        )
        expected = default_command_with_data(**expected_data)

        self.assertEqual(CommandsEndImpersonation(context).call(options), expected)

    def test_call_no_event(self):
        context = {}
        options = default_options()
        options.pop('user_id')

        with self.assertRaises(InvalidParametersError):
            CommandsEndImpersonation(context).call(options)

    def test_call_no_context_ip(self):
        context = {}
        options = default_options()
        options['context'].pop('ip')

        with self.assertRaises(InvalidParametersError):
            CommandsEndImpersonation(context).call(options)

    def test_call_no_context_user_agent(self):
        context = {}
        options = default_options()
        options['context'].pop('user_agent')

        with self.assertRaises(InvalidParametersError):
            CommandsEndImpersonation(context).call(options)
