from castle.configuration import configuration
from castle.api import Api
from castle.context.default import ContextDefault
from castle.context.merger import ContextMerger
from castle.commands.authenticate import CommandsAuthenticate
from castle.commands.identify import CommandsIdentify
from castle.commands.track import CommandsTrack
from castle.exceptions import InternalServerError
from castle.failover_response import FailoverResponse


class Client(object):
    def __init__(self, request, options):
        self.options = options or dict()
        self.do_not_track = self.default_tracking()
        self.context = self.setup_context(request)
        self.api = Api()

    def identify(self, options):
        if not self.tracked():
            return
        return self.api.call(CommandsIdentify(self.context).build(options))

    def authenticate(self, options):
        if self.tracked():
            try:
                response = self.api.call(CommandsAuthenticate(self.context).build(options))
                response.update(failover=False, failover_reason=None)
                return response
            except InternalServerError as exception:
                return self.failover(options, exception)
        else:
            return FailoverResponse(options['user_id'], 'allow', 'Castle set to do not track.').call()

    def track(self, options):
        if not self.tracked():
            return
        return self.api.call(CommandsTrack(self.context).build(options))

    def disable_tracking(self):
        self.do_not_track = True

    def enable_tracking(self):
        self.do_not_track = False

    def tracked(self):
        return not self.do_not_track

    def default_tracking(self):
        return self.options['do_not_track'] if 'do_not_track' in self.options else False

    def setup_context(self, request):
        default_context = ContextDefault(request, self.options.get('cookies', dict())).call()
        return ContextMerger(default_context).call(self.options.get('context', dict()))

    def failover(self, options, exception):
        if configuration.failover_strategy != 'throw':
            return FailoverResponse(options['user_id'], None, exception.__class__.__name__).call()
        raise exception
