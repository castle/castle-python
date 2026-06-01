from castle.test import unittest
from castle.command import Command
from castle.commands.privacy.request_data import CommandsPrivacyRequestData
from castle.commands.privacy.delete_data import CommandsPrivacyDeleteData
from castle.errors import InvalidParametersError


class CommandsPrivacyTestCase(unittest.TestCase):
    def test_request_data(self):
        options = {'identifier': 'a@b.com', 'identifier_type': '$email'}
        self.assertEqual(
            CommandsPrivacyRequestData.call(options),
            Command(method='post', path='privacy/users', data=options),
        )

    def test_request_data_missing_required(self):
        with self.assertRaises(InvalidParametersError):
            CommandsPrivacyRequestData.call({'identifier': 'a@b.com'})

    def test_delete_data(self):
        options = {'identifier': 'a@b.com', 'identifier_type': '$email'}
        self.assertEqual(
            CommandsPrivacyDeleteData.call(options),
            Command(method='delete', path='privacy/users', data=options),
        )

    def test_delete_data_missing_required(self):
        with self.assertRaises(InvalidParametersError):
            CommandsPrivacyDeleteData.call({'identifier_type': '$email'})
