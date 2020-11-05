from castle.test import unittest
from castle.utils2.merge import UtilsMerge


class DeepMergeTestCase(unittest.TestCase):
    def test_simple_merge(self):
        a = {'key': 'value'}
        b = {'otherkey': 'othervalue'}
        UtilsMerge.call(a, b)

        expected = {'key': 'value', 'otherkey': 'othervalue'}
        self.assertEqual(a, expected)

    def test_merge_list(self):
        # Lists are treated as opaque data and so no effort should be made to
        # combine them.
        a = {'key': ['original']}
        b = {'key': ['new']}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': ['new']})

    def test_merge_number(self):
        # The value from b is always taken
        a = {'key': 10}
        b = {'key': 45}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': 45})

        a = {'key': 45}
        b = {'key': 10}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': 10})

    def test_merge_boolean(self):
        # The value from b is always taken
        a = {'key': False}
        b = {'key': True}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': True})

        a = {'key': True}
        b = {'key': False}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': False})

    def test_merge_string(self):
        a = {'key': 'value'}
        b = {'key': 'othervalue'}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': 'othervalue'})

    def test_merge_when_no_extra(self):
        a = {'key': 'value'}
        b = None
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': 'value'})

    def test_merge_none_deletes_from_base(self):
        a = {'key': 'value', 'other': 'value'}
        b = {'other': None}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': 'value'})

    def test_merge_overrides_value(self):
        # The value from b is always taken, even when it's a different type
        a = {'key': 'original'}
        b = {'key': {'newkey': 'newvalue'}}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': {'newkey': 'newvalue'}})

        a = {'key': {'anotherkey': 'value'}}
        b = {'key': 'newvalue'}
        UtilsMerge.call(a, b)
        self.assertEqual(a, {'key': 'newvalue'})

    def test_deep_merge(self):
        a = {
            'first': {
                'second': {
                    'key': 'value',
                    'otherkey': 'othervalue'
                },
                'key': 'value'
            }
        }
        b = {
            'first': {
                'second': {
                    'otherkey': 'newvalue',
                    'yetanotherkey': 'yetanothervalue'
                }
            }
        }
        UtilsMerge.call(a, b)

        expected = {
            'first': {
                'second': {
                    'key': 'value',
                    'otherkey': 'newvalue',
                    'yetanotherkey': 'yetanothervalue'
                },
                'key': 'value'
            }
        }
        self.assertEqual(a, expected)
