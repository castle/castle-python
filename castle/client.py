from castle.configuration import configuration
from castle.commands.authenticate import CommandsAuthenticate
from castle.commands.identify import CommandsIdentify
from castle.commands.track import CommandsTrack
from castle.failover_response import FailoverResponse


class Client(object):
    def __init__(self, request, options=dict()):
        self.options = options or dict()
        self.do_not_track = default_tracking(options)
        self.context = setup_context(request, options)
        self.api = Api(self.castle_headers)

    def fetch_review(self, review_id):
        return self.api.request_query('review/{review_id}')

    def identify(self):
        if not self.tracked:
            return
        return self.api.request(CommandsIdentify(self.context).call(self.options))

    def authenticate(self):
        if self.tracked:
            try:
                return self.api.request(CommandsAuthenticate(self.context).call(self.options))
            except RequestError as exception:
                return self.failover(exception)
        else:
            return FailoverResponse(self.options['user_id'], 'allow').call()

    def track(self):
        if not self.tracked:
            return
        return self.api.request(CommandsTrack(self.context).call(self.options))

    def disable_tracking(self):
        self.do_not_track = True

    def enable_tracking(self):
        self.do_not_track = False

    def tracked(self):
        return not self.do_not_track

    def failover(self, exception):
        if configuration.failover_strategy != 'throw':
            return FailoverResponse(self.options['user_id']).call()
        raise exception
