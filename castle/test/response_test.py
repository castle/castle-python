import io
import requests

from castle.test import unittest
from castle.response import Response
from castle.exceptions import BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, \
    UserUnauthorizedError, InvalidParametersError, InternalServerError


def response(status_code=200, body=None):
    resp = requests.Response()
    resp.raw = io.BytesIO(body)
    resp.status_code = status_code
    return resp


class ResponseTestCase(unittest.TestCase):
    def test_response_none(self):
        self.assertEqual(Response(response()).call(), {})

    def test_response_empty(self):
        self.assertEqual(Response(response(body=b'')).call(), {})

    def test_response_authenticate(self):
        self.assertEqual(
            Response(
                response(body=b'{"action":"allow","user_id":"12345"}')).call(),
            {"action": "allow", "user_id": "12345"}
        )

    def test_verify_200_299(self):
        for status_code in range(200, 299):
            self.assertEqual(
                Response(response(status_code=status_code)).verify(), None)

    def test_verify_400(self):
        with self.assertRaises(BadRequestError):
            Response(response(status_code=400)).verify()

    def test_verify_401(self):
        with self.assertRaises(UnauthorizedError):
            Response(response(status_code=401)).verify()

    def test_verify_403(self):
        with self.assertRaises(ForbiddenError):
            Response(response(status_code=403)).verify()

    def test_verify_404(self):
        with self.assertRaises(NotFoundError):
            Response(response(status_code=404)).verify()

    def test_verify_419(self):
        with self.assertRaises(UserUnauthorizedError):
            Response(response(status_code=419)).verify()

    def test_verify_422(self):
        with self.assertRaises(InvalidParametersError):
            Response(response(status_code=422)).verify()

    def test_verify_500(self):
        with self.assertRaises(InternalServerError):
            Response(response(status_code=500)).verify()
