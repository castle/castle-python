from castle.api_request import APIRequest
from castle.commands.review import CommandsReview
from castle.configuration import configuration


class APIReview(object):
    @staticmethod
    def call(review_id, config=configuration):
        return APIRequest(config).call(CommandsReview.call(review_id))
