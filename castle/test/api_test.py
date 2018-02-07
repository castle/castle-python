from requests import Response
import responses

from castle.test import unittest
from castle.api import Api
from castle.command import Command
from castle.request import Request


def command():
    return Command(method='post', path='authenticate', data={})


def response_text():
    return 'authenticate'


class ApiTestCase(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Api().req, Request)

    @responses.activate
    def test_request(self):
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text(),
            status=200
        )
        self.assertIsInstance(Api().request(command()), Response)

    @responses.activate
    def test_call(self):
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text(),
            status=200
        )
        self.assertEqual(Api().call(command()), response_text())
