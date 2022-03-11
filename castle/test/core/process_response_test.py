import io
import requests

from castle.test import unittest
from castle.core.process_response import CoreProcessResponse
from castle.errors import BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, \
    UserUnauthorizedError, InvalidParametersError, InternalServerError, InvalidRequestTokenError


def response(status_code=200, body=None):
    resp = requests.Response()
    resp.raw = io.BytesIO(body)
    resp.status_code = status_code
    return resp


class CoreProcessResponseTestCase(unittest.TestCase):
    def test_response_none(self):
        self.assertEqual(CoreProcessResponse(response()).call(), {})

    def test_response_empty(self):
        self.assertEqual(CoreProcessResponse(response(body=b'')).call(), {})

    def test_response_authenticate_allow(self):
        self.assertEqual(
            CoreProcessResponse(
                response(body=b'{"action":"allow","user_id":"12345"}')).call(),
            {"action": "allow", "user_id": "12345"}
        )

    def test_response_authenticate_allow_with_props(self):
        self.assertEqual(
            CoreProcessResponse(
                response(body=b'{"action":"allow","user_id":"12345","internal":{}}')).call(),
            {"action": "allow", "user_id": "12345", "internal": {}}
        )

    def test_response_authenticate_deny_without_rp(self):
        self.assertEqual(
            CoreProcessResponse(
                response(body=b'{"action":"deny","user_id":"1","device_token":"abc"}')).call(),
            {"action": "deny", "user_id": "1", "device_token": "abc"}
        )

    def test_response_authenticate_deny_with_rp(self):
        self.assertEqual(
            CoreProcessResponse(
                response(body=b'{"action":"deny","user_id":"1","device_token":"abc","risk_policy":{"id":"123","revision_id":"abc","name":"def","type":"bot"}}')).call(),
            {"action": "deny", "user_id": "1", "device_token": "abc", "risk_policy": {
                "id": "123", "revision_id": "abc", "name": "def", "type": "bot"}}
        )

    def test_verify_200_299(self):
        for status_code in range(200, 299):
            self.assertEqual(
                CoreProcessResponse(response(status_code=status_code)).verify(), None)

    def test_verify_400(self):
        with self.assertRaises(BadRequestError):
            CoreProcessResponse(response(status_code=400)).verify()

    def test_verify_401(self):
        with self.assertRaises(UnauthorizedError):
            CoreProcessResponse(response(status_code=401)).verify()

    def test_verify_403(self):
        with self.assertRaises(ForbiddenError):
            CoreProcessResponse(response(status_code=403)).verify()

    def test_verify_404(self):
        with self.assertRaises(NotFoundError):
            CoreProcessResponse(response(status_code=404)).verify()

    def test_verify_419(self):
        with self.assertRaises(UserUnauthorizedError):
            CoreProcessResponse(response(status_code=419)).verify()

    def test_verify_422(self):
        with self.assertRaises(InvalidParametersError):
            CoreProcessResponse(response(status_code=422)).verify()

    def test_verify_422_record_invalid(self):
        with self.assertRaises(InvalidParametersError):
            CoreProcessResponse(response(status_code=422, body=b'{"type":"record_invalid","message":"validation failed"}')).verify()

    def test_verify_422_invalid_request_token(self):
        with self.assertRaises(InvalidRequestTokenError):
            CoreProcessResponse(response(status_code=422, body=b'{"type":"invalid_request_token","message":"token invalid"}')).verify()


    def test_verify_500(self):
        with self.assertRaises(InternalServerError):
            CoreProcessResponse(response(status_code=500)).verify()
