import base64
import hashlib
import binascii
import hmac

from castle.configuration import configuration
from castle.core.process_webhook import CoreProcessWebhook
from castle.errors import WebhookVerificationError
from castle.utils.secure_compare import UtilsSecureCompare


class WebhooksVerify(object):
    @classmethod
    def call(cls, webhook):
        expected_signature = cls._compute_signature(webhook)
        signature = webhook.headers.get('X-Castle-Signature')
        return cls._verify_signature(signature, expected_signature)

    @staticmethod
    def _compute_signature(webhook):
        encoded_str = hmac.new(
            bytes(configuration.api_secret.encode('utf-8')),
            CoreProcessWebhook(webhook).call(),
            hashlib.sha256
        ).hexdigest()
        return base64.b64encode(binascii.unhexlify(encoded_str)).decode('utf-8')

    @staticmethod
    def _verify_signature(signature, expected_signature):
        if UtilsSecureCompare.call(signature, expected_signature):
            return

        raise WebhookVerificationError("Invalid webhook from Castle API")
