from castle.test import unittest
from castle.validators.present import ValidatorsPresent
from castle.exceptions import InvalidParametersError


class ValidatorsPresentTestCase(unittest.TestCase):

    def test_call_valid(self):
        params = {'foo': 'bar', 'fooz': 'barz'}
        self.assertEqual(
            ValidatorsPresent.call(params, 'foo', 'fooz'),
            None
        )

    def test_call_not_valid(self):
        params = {'foo': 'bar', 'fooz': 'barz'}

        with self.assertRaises(InvalidParametersError):
            ValidatorsPresent.call(params, 'foo', 'missing')
