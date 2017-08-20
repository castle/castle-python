from castle.test import unittest

from castle.context.merger import ContextMerger


class ContextMergerTestCase(unittest.TestCase):
    def test_init(self):
        params = {'foo': 'bar'}
        self.assertIsNot(ContextMerger(params).source_copy, params)

    def test_call(self):
        params = {'foo': 'bar'}
        self.assertEqual(ContextMerger(params).call({'foo': 'foo'}), {'foo': 'foo'})
