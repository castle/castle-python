from castle.errors import APIError
from castle.logger import Logger


class CoreProcessWebhook(object):
    def __init__(self, webhook):
        self.webhook = webhook

    def call(self):
        self.verify()

        Logger.call("webhook:", self.webhook.data)
        return self.webhook.data

    def verify(self):
        if self.webhook.data is not None and len(self.webhook.data) != 0:
            return

        raise APIError("Invalid webhook from Castle API")
