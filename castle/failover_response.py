from castle.configuration import configuration


class FailoverResponse(object):
    def __init__(self, user_id, strategy=None):
        self.strategy = strategy or configuration.failover_strategy
        self.user_id = user_id

    def call(self):
        return {'action': self.strategy, 'user_id': self.user_id}
