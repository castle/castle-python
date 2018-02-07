from castle.test import unittest
from castle.command import Command


def command():
    return Command(
        method='post',
        path='authenticate',
        data={'event': '$login.authenticate'}
    )


class CommandTestCase(unittest.TestCase):
    def test_create_command(self):
        self.assertEqual(command().method, 'post')
        self.assertEqual(command().path, 'authenticate')
        self.assertEqual(command().data, {'event': '$login.authenticate'})
