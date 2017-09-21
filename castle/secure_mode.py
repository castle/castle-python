import hmac

from castle.configuration import configuration


def signature(user_id):
    return hmac.new(
        bytes(configuration.api_secret, encoding='utf-8'),
        bytes(user_id, encoding='utf-8'),
        'sha256'
    ).hexdigest()
