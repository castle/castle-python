import hmac
import hashlib

from castle.configuration import configuration


def signature(user_id, config = configuration):
    return hmac.new(
        bytes(config.api_secret.encode('utf-8')),
        bytes(user_id.encode('utf-8')),
        hashlib.sha256
    ).hexdigest()
