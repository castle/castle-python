from castle.configuration import configuration


class FailoverPrepareResponse(object):
    def __init__(self, user_id, strategy=None, reason=None):
        self.strategy = strategy or configuration.failover_strategy
        self.reason = reason
        self.user_id = user_id

    def call(self):
        return dict(
            policy={'action': self.strategy},
            action=self.strategy,
            user_id=self.user_id,
            failover=True,
            failover_reason=self.reason
        )
