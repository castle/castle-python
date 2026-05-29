from castle.api_request import APIRequest
from castle.commands.filter import CommandsFilter
from castle.commands.log import CommandsLog
from castle.commands.risk import CommandsRisk
from castle.commands.lists.create import CommandsListsCreate
from castle.commands.lists.get_all import CommandsListsGetAll
from castle.commands.lists.get import CommandsListsGet
from castle.commands.lists.query import CommandsListsQuery
from castle.commands.lists.update import CommandsListsUpdate
from castle.commands.lists.delete import CommandsListsDelete
from castle.commands.list_items.create import CommandsListItemsCreate
from castle.commands.list_items.create_batch import CommandsListItemsCreateBatch
from castle.commands.list_items.get import CommandsListItemsGet
from castle.commands.list_items.query import CommandsListItemsQuery
from castle.commands.list_items.count import CommandsListItemsCount
from castle.commands.list_items.update import CommandsListItemsUpdate
from castle.commands.list_items.archive import CommandsListItemsArchive
from castle.commands.list_items.unarchive import CommandsListItemsUnarchive
from castle.commands.privacy.request_data import CommandsPrivacyRequestData
from castle.commands.privacy.delete_data import CommandsPrivacyDeleteData
from castle.configuration import configuration
from castle.context.prepare import ContextPrepare
from castle.errors import InternalServerError, RequestError
from castle.failover.prepare_response import FailoverPrepareResponse
from castle.failover.strategy import FailoverStrategy


class Client(object):
    @classmethod
    def from_request(cls, request, options=None):
        if options is None:
            options = {}

        options = options.copy()
        options['context'] = ContextPrepare.call(request, options)
        return cls(options)

    @staticmethod
    def failover_response_or_raise(user_id, exception):
        if configuration.failover_strategy == FailoverStrategy.THROW.value:
            raise exception
        return FailoverPrepareResponse(user_id, None, exception.__class__.__name__).call()

    def __init__(self, options=None):
        if options is None:
            options = {}
        self.do_not_track = options.get('do_not_track', False)
        self.timestamp = options.get('timestamp')
        self.context = options.get('context')
        self.api = APIRequest()

    def _add_timestamp_if_necessary(self, options):
        if self.timestamp:
            options.setdefault('timestamp', self.timestamp)

    def filter(self, options):
        if self.tracked():
            self._add_timestamp_if_necessary(options)
            command = CommandsFilter(self.context).call(options)
            try:
                response = self.api.call(command)
                response.update(failover=False, failover_reason=None)
                return response
            except (RequestError, InternalServerError) as exception:
                return Client.failover_response_or_raise(self._failover_user_id(options), exception)
        else:
            return FailoverPrepareResponse(
                self._failover_user_id(options), 'allow', 'Castle set to do not track.'
            ).call()

    def log(self, options):
        if not self.tracked():
            return None
        self._add_timestamp_if_necessary(options)

        return self.api.call(CommandsLog(self.context).call(options))

    def risk(self, options):
        if self.tracked():
            self._add_timestamp_if_necessary(options)
            command = CommandsRisk(self.context).call(options)
            try:
                response = self.api.call(command)
                response.update(failover=False, failover_reason=None)
                return response
            except (RequestError, InternalServerError) as exception:
                return Client.failover_response_or_raise(self._failover_user_id(options), exception)
        else:
            return FailoverPrepareResponse(
                self._failover_user_id(options), 'allow', 'Castle set to do not track.'
            ).call()

    def create_list(self, options):
        return self.api.call(CommandsListsCreate.call(options))

    def get_all_lists(self, options=None):
        return self.api.call(CommandsListsGetAll.call(options))

    def get_list(self, options):
        return self.api.call(CommandsListsGet.call(options))

    def query_lists(self, options):
        return self.api.call(CommandsListsQuery.call(options))

    def update_list(self, options):
        return self.api.call(CommandsListsUpdate.call(options))

    def delete_list(self, options):
        return self.api.call(CommandsListsDelete.call(options))

    def create_list_item(self, options):
        return self.api.call(CommandsListItemsCreate.call(options))

    def create_batch_list_items(self, options):
        return self.api.call(CommandsListItemsCreateBatch.call(options))

    def get_list_item(self, options):
        return self.api.call(CommandsListItemsGet.call(options))

    def query_list_items(self, options):
        return self.api.call(CommandsListItemsQuery.call(options))

    def count_list_items(self, options):
        return self.api.call(CommandsListItemsCount.call(options))

    def update_list_item(self, options):
        return self.api.call(CommandsListItemsUpdate.call(options))

    def archive_list_item(self, options):
        return self.api.call(CommandsListItemsArchive.call(options))

    def unarchive_list_item(self, options):
        return self.api.call(CommandsListItemsUnarchive.call(options))

    def request_user_data(self, options):
        return self.api.call(CommandsPrivacyRequestData.call(options))

    def delete_user_data(self, options):
        return self.api.call(CommandsPrivacyDeleteData.call(options))

    def disable_tracking(self):
        self.do_not_track = True

    def enable_tracking(self):
        self.do_not_track = False

    def tracked(self):
        return not self.do_not_track

    @staticmethod
    def _failover_user_id(options):
        # `user` is optional on /v1/filter and may be omitted on /v1/log; fall
        # back to `matching_user_id` then None instead of crashing.
        user = options.get('user') or {}
        return user.get('id') or options.get('matching_user_id')
