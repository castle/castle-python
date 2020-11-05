from datetime import datetime

from castle.test import mock, unittest
from castle.utils2.clone import UtilsClone


class UtilsCloneTestCase(unittest.TestCase):
    def test_clone(self):
        params = {'foo': 'bar'}
        new_params = UtilsClone.call(params)
        self.assertEqual(params, new_params)
        self.assertIsNot(new_params, params)
