import warnings
from castle.configuration import configuration
from castle.api_request import APIRequest
from castle.context.get_default import ContextGetDefault
from castle.context.merge import ContextMerge
from castle.commands.authenticate import CommandsAuthenticate
from castle.commands.identify import CommandsIdentify
from castle.commands.start_impersonation import CommandsStartImpersonation
from castle.commands.end_impersonation import CommandsEndImpersonation
from castle.commands.track import CommandsTrack
from castle.errors import InternalServerError, RequestError, ImpersonationFailed
from castle.failover.prepare_response import FailoverPrepareResponse
from castle.failover.strategy import FailoverStrategy
from castle.utils.timestamp import UtilsTimestamp as generate_timestamp


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
        default_context = ContextGetDefault(
            request, options.get('cookies')).call()
        return ContextMerge.call(default_context, options.get('context', {}))

    @staticmethod
    def to_options(options=None):
        if options is None:
            options = {}
        options.setdefault('timestamp', generate_timestamp.call())
        if 'traits' in options:
            warnings.warn('use user_traits instead of traits key', DeprecationWarning)

        return options

    @staticmethod
    def failover_response_or_raise(options, exception):
        if configuration.failover_strategy == FailoverStrategy.THROW.value:
            raise exception
        return FailoverPrepareResponse(
            options.get('user_id'), None, exception.__class__.__name__
        ).call()

    def __init__(self, context, options=None):
        if options is None:
            options = {}
        self.do_not_track = options.get('do_not_track', False)
        self.timestamp = options.get('timestamp')
        self.context = context
        self.api = APIRequest()

    def _add_timestamp_if_necessary(self, options):
        if self.timestamp:
            options.setdefault('timestamp', self.timestamp)

    def authenticate(self, options):
        if self.tracked():
            self._add_timestamp_if_necessary(options)
            command = CommandsAuthenticate(self.context).call(options)
            try:
                response = self.api.call(command)
                response.update(failover=False, failover_reason=None)
                return response
            except (RequestError, InternalServerError) as exception:
                return Client.failover_response_or_raise(options, exception)
        else:
            return FailoverPrepareResponse(
                options.get('user_id'),
                'allow',
                'Castle set to do not track.'
            ).call()

    def identify(self, options):
        if not self.tracked():
            return None
        self._add_timestamp_if_necessary(options)
        return self.api.call(CommandsIdentify(self.context).call(options))

    def start_impersonation(self, options):
        self._add_timestamp_if_necessary(options)
        response = self.api.call(CommandsStartImpersonation(self.context).call(options))
        if not response.get('success'):
            raise ImpersonationFailed
        return response

    def end_impersonation(self, options):
        self._add_timestamp_if_necessary(options)
        response = self.api.call(CommandsEndImpersonation(self.context).call(options))
        if not response.get('success'):
            raise ImpersonationFailed
        return response

    def track(self, options):
        if not self.tracked():
            return None
        self._add_timestamp_if_necessary(options)
        return self.api.call(CommandsTrack(self.context).call(options))

    def disable_tracking(self):
        self.do_not_track = True

    def enable_tracking(self):
        self.do_not_track = False

    def tracked(self):
        return not self.do_not_track
