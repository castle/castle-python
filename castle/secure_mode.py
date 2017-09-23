import hmac
import hashlib

from castle.configuration import configuration


def signature(user_id):
    return hmac.new(
        bytes(configuration.api_secret.encode('utf-8')),
        bytes(user_id.encode('utf-8')),
        hashlib.sha256
    ).hexdigest()
