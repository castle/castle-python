from castle.test import unittest
from castle.command import Command
from castle.commands.review import CommandsReview
from castle.errors import InvalidParametersError


def review_id():
    return '1234'


class CommandsReviewTestCase(unittest.TestCase):
    def test_call_no_review_id(self):
        with self.assertRaises(InvalidParametersError):
            CommandsReview.call('')

    def test_call(self):
        command = CommandsReview.call(review_id())
        self.assertIsInstance(command, Command)
        self.assertEqual(command.method, 'get')
        self.assertEqual(command.path, "reviews/1234")
        self.assertEqual(command.data, None)
