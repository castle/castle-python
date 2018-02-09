from castle.test import unittest
from castle.context.sanitizer import ContextSanitizer


class ContextSanitizerTestCase(unittest.TestCase):

    def test_call_when_no_context(self):
        context = None
        self.assertEqual(ContextSanitizer.call(context), {})

    def test_call_when_no_active_context(self):
        context = {'foo': 'bar'}
        self.assertEqual(ContextSanitizer.call(context), {'foo': 'bar'})

    def test_call_when_no_active_is_string(self):
        context = {'foo': 'bar', 'active': 'true'}
        self.assertEqual(ContextSanitizer.call(context), {'foo': 'bar'})

    def test_call_when_have_active_flag(self):
        context = {'foo': 'bar', 'active': True}
        self.assertEqual(ContextSanitizer.call(context),
                         {'foo': 'bar', 'active': True})
