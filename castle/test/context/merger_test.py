from castle.test import unittest
from castle.context.merger import ContextMerger


class ContextMergerTestCase(unittest.TestCase):

    def test_call(self):
        params = {'foo': {'foo': 'bar', 'nonfoo': 'nonbar'}, 'to_remove': 'ok'}
        self.assertEqual(
            ContextMerger.call(
                params, {'foo': {'foo': 'foo'}, 'to_remove': None}),
            {'foo': {'foo': 'foo', 'nonfoo': 'nonbar'}}
        )
