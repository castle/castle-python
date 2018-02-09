from castle.test import unittest
from castle.validators.not_supported import ValidatorsNotSupported
from castle.exceptions import InvalidParametersError


class ValidatorsNotSupportedTestCase(unittest.TestCase):

    def test_call_valid(self):
        params = {'foo': 'bar', 'fooz': 'barz'}
        self.assertEqual(
            ValidatorsNotSupported.call(params, 'unknown', 'unknown1'),
            None
        )

    def test_call_not_valid(self):
        params = {'foo': 'bar', 'fooz': 'barz'}

        with self.assertRaises(InvalidParametersError):
            ValidatorsNotSupported.call(params, 'unknown', 'foo')
