from datetime import datetime

from castle.test import mock, unittest
from castle.utils import clone, deep_merge, timestamp


class UtilsTestCase(unittest.TestCase):
    def test_clone(self):
        params = {'foo': 'bar'}
        new_params = clone(params)
        self.assertEqual(params, new_params)
        self.assertIsNot(new_params, params)


class DeepMergeTestCase(unittest.TestCase):
    def test_simple_merge(self):
        a = {'key': 'value'}
        b = {'otherkey': 'othervalue'}
        deep_merge(a, b)

        expected = {'key': 'value', 'otherkey': 'othervalue'}
        self.assertEqual(a, expected)

    def test_merge_list(self):
        # Lists are treated as opaque data and so no effort should be made to
        # combine them.
        a = {'key': ['original']}
        b = {'key': ['new']}
        deep_merge(a, b)
        self.assertEqual(a, {'key': ['new']})

    def test_merge_number(self):
        # The value from b is always taken
        a = {'key': 10}
        b = {'key': 45}
        deep_merge(a, b)
        self.assertEqual(a, {'key': 45})

        a = {'key': 45}
        b = {'key': 10}
        deep_merge(a, b)
        self.assertEqual(a, {'key': 10})

    def test_merge_boolean(self):
        # The value from b is always taken
        a = {'key': False}
        b = {'key': True}
        deep_merge(a, b)
        self.assertEqual(a, {'key': True})

        a = {'key': True}
        b = {'key': False}
        deep_merge(a, b)
        self.assertEqual(a, {'key': False})

    def test_merge_string(self):
        a = {'key': 'value'}
        b = {'key': 'othervalue'}
        deep_merge(a, b)
        self.assertEqual(a, {'key': 'othervalue'})

    def test_merge_when_no_extra(self):
        a = {'key': 'value'}
        b = None
        deep_merge(a, b)
        self.assertEqual(a, {'key': 'value'})

    def test_merge_none_deletes_from_base(self):
        a = {'key': 'value', 'other': 'value'}
        b = {'other': None}
        deep_merge(a, b)
        self.assertEqual(a, {'key': 'value'})

    def test_merge_overrides_value(self):
        # The value from b is always taken, even when it's a different type
        a = {'key': 'original'}
        b = {'key': {'newkey': 'newvalue'}}
        deep_merge(a, b)
        self.assertEqual(a, {'key': {'newkey': 'newvalue'}})

        a = {'key': {'anotherkey': 'value'}}
        b = {'key': 'newvalue'}
        deep_merge(a, b)
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
        deep_merge(a, b)

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


class TimestampTestCase(unittest.TestCase):

    @mock.patch('castle.utils.datetime')
    def test_it_should_use_iso_format(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(
            2018, 1, 2, 3, 4, 5, 678901)
        expected = '2018-01-02T03:04:05.678901'
        self.assertEqual(timestamp(), expected)
