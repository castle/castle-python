from castle.configuration import configuration
from castle.api import Api
from castle.context.default import ContextDefault
from castle.context.merger import ContextMerger
from castle.commands.authenticate import CommandsAuthenticate
from castle.commands.identify import CommandsIdentify
from castle.commands.impersonate import CommandsImpersonate
from castle.commands.track import CommandsTrack
from castle.exceptions import InternalServerError, RequestError, ImpersonationFailed
from castle.failover_response import FailoverResponse
from castle.utils import timestamp as generate_timestamp
import warnings

class Client(object):

    @classmethod
    def from_request(cls, request, options=None):
        if options is None:
            options = {}
        return cls(
            cls.to_context(request, options),
            cls.to_options(options)
        )

    @staticmethod
    def to_context(request, options=None):
        if options is None:
            options = {}
        default_context = ContextDefault(
            request, options.get('cookies')).call()
        return ContextMerger.call(default_context, options.get('context', {}))

    @staticmethod
    def to_options(options=None):
        if options is None:
            options = {}
        options.setdefault('timestamp', generate_timestamp())
        if 'traits' in options:
            warnings.warn('use user_traits instead of traits key', DeprecationWarning)

        return options

    @staticmethod
    def failover_response_or_raise(options, exception):
        if configuration.failover_strategy == 'throw':
            raise exception
        return FailoverResponse(options.get('user_id'), None, exception.__class__.__name__).call()

    def __init__(self, context, options=None):
        if options is None:
            options = {}
        self.do_not_track = options.get('do_not_track', False)
        self.timestamp = options.get('timestamp')
        self.context = context
        self.api = Api()

    def _add_timestamp_if_necessary(self, options):
        if self.timestamp:
            options.setdefault('timestamp', self.timestamp)

    def authenticate(self, options):
        if self.tracked():
            self._add_timestamp_if_necessary(options)
            command = CommandsAuthenticate(self.context).build(options)
            try:
                response = self.api.call(command)
                response.update(failover=False, failover_reason=None)
                return response
            except (RequestError, InternalServerError) as exception:
                return Client.failover_response_or_raise(options, exception)
        else:
            return FailoverResponse(
                options.get('user_id'),
                'allow',
                'Castle set to do not track.'
            ).call()

    def identify(self, options):
        if not self.tracked():
            return None
        self._add_timestamp_if_necessary(options)
        return self.api.call(CommandsIdentify(self.context).build(options))

    def impersonate(self, options):
        self._add_timestamp_if_necessary(options)
        response = self.api.call(CommandsImpersonate(self.context).build(options))
        if not response.get('success'):
            raise ImpersonationFailed
        return response

    def track(self, options):
        if not self.tracked():
            return None
        self._add_timestamp_if_necessary(options)
        return self.api.call(CommandsTrack(self.context).build(options))

    def disable_tracking(self):
        self.do_not_track = True

    def enable_tracking(self):
        self.do_not_track = False

    def tracked(self):
        return not self.do_not_track
