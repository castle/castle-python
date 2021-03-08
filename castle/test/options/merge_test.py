from castle.test import unittest
from castle.options.merge import OptionsMerge


class OptionsMergeTestCase(unittest.TestCase):

    def test_call(self):
        params = {'foo': {'foo': 'bar', 'nonfoo': 'nonbar'}, 'to_remove': 'ok'}
        self.assertEqual(
            OptionsMerge.call(
                params, {'foo': {'foo': 'foo'}, 'to_remove': None}),
            {'foo': {'foo': 'foo', 'nonfoo': 'nonbar'}}
        )
