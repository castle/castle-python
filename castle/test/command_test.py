from castle.test import unittest
from castle.command import Command


class CommandTestCase(unittest.TestCase):
    def command(self):
        return Command(method='post', endpoint='authenticate', data={'event': '$login.authenticate'})

    def test_create_command(self):
        self.assertEqual(self.command().method, 'post')
        self.assertEqual(self.command().endpoint, 'authenticate')
        self.assertEqual(self.command().data, {'event': '$login.authenticate'})
