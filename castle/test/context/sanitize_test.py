from castle.test import unittest
from castle.context.sanitize import ContextSanitize


class ContextSanitizeTestCase(unittest.TestCase):

    def test_call_when_no_context(self):
        context = None
        self.assertEqual(ContextSanitize.call(context), {})

    def test_call_when_no_active_context(self):
        context = {'foo': 'bar'}
        self.assertEqual(ContextSanitize.call(context), {'foo': 'bar'})

    def test_call_when_no_active_is_string(self):
        context = {'foo': 'bar', 'active': 'true'}
        self.assertEqual(ContextSanitize.call(context), {'foo': 'bar'})

    def test_call_when_have_active_flag(self):
        context = {'foo': 'bar', 'active': True}
        self.assertEqual(ContextSanitize.call(context),
                         {'foo': 'bar', 'active': True})
