from castle.configuration import configuration
from castle.api import Api
from castle.context.default import ContextDefault
from castle.context.merger import ContextMerger
from castle.commands.authenticate import CommandsAuthenticate
from castle.commands.identify import CommandsIdentify
from castle.commands.track import CommandsTrack
from castle.exceptions import InternalServerError
from castle.failover_response import FailoverResponse
from castle.utils import timestamp


class Client(object):

    @classmethod
    def from_request(cls, request, options={}):
        return cls(
            cls.build_client_context(request, options),
            cls.build_client_options(options)
        )

    @classmethod
    def build_client_context(cls, request, options={}):
        default_context = ContextDefault(request, cls.build_client_cookies(request, options)).call()
        return ContextMerger(default_context).call(options.get('context', {}))

    @classmethod
    def build_client_options(cls, options={}):
        options['timestamp'] = timestamp()
        return options

    @classmethod
    def build_client_cookies(cls, request, options={}):
        # if the request has use them
        if hasattr(request, 'COOKIES') and request.COOKIES:
            return request.COOKIES

        # else, they may have been passed in as options
        return options.get('cookies', {})

    def __init__(self, context, options={}):
        self.do_not_track = options.get('do_not_track', False)
        self.timestamp = options.get('timestamp')
        self.context = context
        self.api = Api()

    def _set_timestamp_if_necessary(self, options):
        if self.timestamp:
            options.setdefault(self.timestamp)

    def authenticate(self, options):
        if self.tracked():
            try:
                self._set_timestamp_if_necessary(options)
                response = self.api.call(CommandsAuthenticate(self.context).build(options))
                response.update(failover=False, failover_reason=None)
                return response
            except InternalServerError as exception:
                return Client.failover(options, exception)
        else:
            return FailoverResponse(
                options['user_id'],
                'allow',
                'Castle set to do not track.'
            ).call()

    def identify(self, options):
        if not self.tracked():
            return
        self._set_timestamp_if_necessary(options)
        return self.api.call(CommandsIdentify(self.context).build(options))

    def track(self, options):
        if not self.tracked():
            return
        self._set_timestamp_if_necessary(options)
        return self.api.call(CommandsTrack(self.context).build(options))

    def disable_tracking(self):
        self.do_not_track = True

    def enable_tracking(self):
        self.do_not_track = False

    def tracked(self):
        return not self.do_not_track

    @staticmethod
    def failover(options, exception):
        if configuration.failover_strategy != 'throw':
            return FailoverResponse(options['user_id'], None, exception.__class__.__name__).call()
        raise exception
