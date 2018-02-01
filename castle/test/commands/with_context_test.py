from castle.commands.with_context import sanitize_active_mode, WithContext
from castle.test import mock, unittest


class SanitizeActiveMode(unittest.TestCase):
    def test_when_active_not_specified_then_options_unmodified(self):
        options = {'context': {'whatever': 'okay'}, 'test': 'nonsense'}
        sanitize_active_mode(options)

        self.assertEqual(options, {'context': {'whatever': 'okay'}, 'test': 'nonsense'})

    def test_when_active_true_then_options_unmodified(self):
        options = {'context': {'active': True}, 'foo': 'spam'}
        sanitize_active_mode(options)

        self.assertEqual(options, {'context': {'active': True}, 'foo': 'spam'})

    def test_when_active_false_then_options_unmodified(self):
        options = {'context': {'active': False}, 'foo': 'spam'}
        sanitize_active_mode(options)

        self.assertEqual(options, {'context': {'active': False}, 'foo': 'spam'})

    def test_when_active_string_then_active_removed(self):
        options = {'context': {'active': 'true'}, 'foo': 'spam'}
        sanitize_active_mode(options)

        self.assertEqual(options, {'context': {}, 'foo': 'spam'})

    def test_when_active_int_then_active_removed(self):
        options = {'context': {'active': 1, 'another thing': 'sure'}, 'frog': 'spawn'}
        sanitize_active_mode(options)

        self.assertEqual(options, {'context': {'another thing': 'sure'}, 'frog': 'spawn'})


class WithContextTestCase(unittest.TestCase):

    @mock.patch('castle.commands.with_context.ContextMerger')
    def test_init(self, mock_ContextMerger):
        mock_ContextMerger.return_value = mock.sentinel.merger_instance

        obj = WithContext(mock.sentinel.context)

        self.assertIs(obj.context_merger, mock.sentinel.merger_instance)
        mock_ContextMerger.assert_called_once_with(mock.sentinel.context)

    def test_build_context(self):
        context = {'thirsty': True}
        options = {'context': {'hungry': True}, 'want': ['pizza', 'beer']}

        # expect the original context to have been merged with the context specified in the options
        expected = {'context': {'thirsty': True, 'hungry': True}, 'want': ['pizza', 'beer']}

        self.assertEqual(WithContext(context).build_context(options), expected)

    @mock.patch('castle.commands.with_context.sanitize_active_mode')
    def test_build_context_sanitizes_active_mode_option(self, mock_sanitize_active_mode):
        context = {}  # doesn't matter for this test
        options = {'context': mock.sentinel.options_context}

        obj = WithContext(context)
        with mock.patch.object(obj, 'merge_context') as mock_merge_context:
            obj.build_context(options)

        mock_sanitize_active_mode.assert_called_once_with(options)
        mock_merge_context.assert_called_once_with(mock.sentinel.options_context)

    def test_build_context_empty_options(self):
        context = {'ambiance': 'smokey'}
        options = {}

        expected = {'context': context}

        self.assertEqual(WithContext(context).build_context(options), expected)

    def test_build_context_override_value(self):
        context = {'mood': 'grumpy', 'sky': 'blue', 'drink': 'none to speak of'}
        options = {'context': {'mood': 'all smiles', 'drink': 3}}

        expected = {'context': {'mood': 'all smiles', 'sky': 'blue', 'drink': 3}}

        self.assertEqual(WithContext(context).build_context(options), expected)

    def test_build_context_options_without_context(self):
        context = {'sleepy': True}
        options = {'giving up': False}

        expected = {'context': {'sleepy': True}, 'giving up': False}

        self.assertEqual(WithContext(context).build_context(options), expected)
