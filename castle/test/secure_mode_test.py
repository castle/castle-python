from castle.test import unittest
from castle.secure_mode import signature

from castle.configuration import configuration


class SecureModeTestCase(unittest.TestCase):
    def test_signature(self):
        configuration.api_secret = 'secret'
        self.assertEqual(
            signature('test'),
            '0329a06b62cd16b33eb6792be8c60b158d89a2ee3a876fce9a881ebb488c0914'
        )
