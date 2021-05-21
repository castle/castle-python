import threading
from requests import Response
import responses
from castle.test import unittest
from castle.core.send_request import CoreSendRequest
from castle.configuration import configuration

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer


def run_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = '{"action":"allow", "user_id": "123"}'.encode()
            self.send_response(201)
            self.send_header('content-type', 'application/json')
            self.send_header('content-length', len(body))
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(('', 65521), SimpleHandler)
    httpd_thread = threading.Thread(target=server.serve_forever)
    httpd_thread.setDaemon(True)
    httpd_thread.start()
    return httpd_thread


class CoreSendRequestTestCase(unittest.TestCase):
    def test_init_headers(self):
        headers = {'X-Castle-Client-Id': '1234'}
        self.assertEqual(CoreSendRequest(headers).headers, headers)

    def test_init_base_url(self):
        self.assertEqual(CoreSendRequest().base_url, 'https://api.castle.io/v1')

    @responses.activate
    def test_build_query(self):
        data = {'event': '$login.authenticate', 'user_id': '12345'}
        configuration.api_secret = 'api_secret'
        # JSON requires double quotes for its strings
        response_text = {"action": "allow", "user_id": "12345"}
        responses.add(
            responses.POST,
            'https://api.castle.io/v1/authenticate',
            json=response_text,
            status=200
        )
        res = CoreSendRequest().build_query('post', 'authenticate', data)
        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), response_text)

        configuration.api_secret = None

    def test_connection_pooled(self):
        configuration.base_url = 'http://localhost:65521'
        run_server()
        request = CoreSendRequest()
        data = {'event': '$login.authenticate', 'user_id': '12345'}
        response = request.build_query('post', 'authenticate', data)
        num_pools = len(response.connection.poolmanager.pools.keys())
        configuration.base_url = 'https://api.castle.io/v1'
        self.assertEqual(num_pools, 1)

    def test_build_url(self):
        self.assertEqual(
            CoreSendRequest().build_url('authenticate'),
            'https://api.castle.io/v1/authenticate'
        )

    def test_build_url_with_port(self):
        configuration.base_url = 'http://api.castle.local:3001'
        self.assertEqual(
            CoreSendRequest().build_url('test'),
            'http://api.castle.local:3001/test'
        )

    def test_verify_true(self):
        self.assertEqual(CoreSendRequest().verify(), True)

    def test_verify_false(self):
        configuration.base_url = 'http://api.castle.io'
        self.assertEqual(CoreSendRequest().verify(), False)
        configuration.base_url = 'https://api.castle.io/v1'
