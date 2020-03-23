from castle.test import unittest, mock
from castle.extractors.ip import ExtractorsIp
from castle.configuration import configuration


class ExtractorsIpTestCase(unittest.TestCase):
    def tearDown(self):
        configuration.ip_headers = []
        configuration.trusted_proxies = []

    def test_extract_ip(self):
        headers = { 'X-Forwarded-For': '1.2.3.5' }
        self.assertEqual(ExtractorsIp(headers).call(), '1.2.3.5')

    def test_extract_ip_when_second_header(self):
        headers =  { 'Cf-Connecting-Ip': '1.2.3.4', 'X-Forwarded-For': '1.1.1.1, 1.2.2.2, 1.2.3.5' }
        configuration.ip_headers = ["HTTP_CF_CONNECTING_IP"]
        self.assertEqual(
            ExtractorsIp(headers).call(),
            '1.2.3.4'
        )
    def test_extract_ip_when_second_header_with_different_setting(self):
        headers =  { 'Cf-Connecting-Ip': '1.2.3.4', 'X-Forwarded-For': '1.1.1.1, 1.2.2.2, 1.2.3.5' }
        configuration.ip_headers = ["CF-CONNECTING-IP"]
        self.assertEqual(
            ExtractorsIp(headers).call(),
            '1.2.3.4'
        )

    def test_extract_ip_when_all_trusted_proxies(self):
        xf_header = '127.0.0.1,10.0.0.1,172.31.0.1,192.168.0.1,::1,fd00::,localhost,unix,unix:/tmp/sock'
        headers =  { 'Remote-Addr': '127.0.0.1', 'X-Forwarded-For': xf_header }
        self.assertEqual(
            ExtractorsIp(headers).call(),
            '127.0.0.1'
        )


    def test_extract_ip_for_spoof_ip_attempt(self):
        headers = { 'Client-Ip': '6.6.6.6', 'X-Forwarded-For': '6.6.6.6, 2.2.2.3, 192.168.0.7' }
        self.assertEqual(
            ExtractorsIp(headers).call(),
            '2.2.2.3'
        )
#
    def test_extract_ip_for_spoof_ip_attempt_when_all_trusted_proxies(self):
        headers = { 'Client-Ip': '6.6.6.6', 'X-Forwarded-For': '6.6.6.6, 2.2.2.3, 192.168.0.7' }
        configuration.trusted_proxies = ['^2.2.2.\d$']
        self.assertEqual(
            ExtractorsIp(headers).call(),
            '6.6.6.6'
        )
