from castle.test import unittest
from castle.context.merge import ContextMerge


class ContextMergeTestCase(unittest.TestCase):

    def test_call(self):
        params = {'foo': {'foo': 'bar', 'nonfoo': 'nonbar'}, 'to_remove': 'ok'}
        self.assertEqual(
            ContextMerge.call(
                params, {'foo': {'foo': 'foo'}, 'to_remove': None}),
            {'foo': {'foo': 'foo', 'nonfoo': 'nonbar'}}
        )
