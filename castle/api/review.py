from castle.api_request import APIRequest
from castle.commands.review import CommandsReview


class APIReview(object):
    @staticmethod
    def call(review_id):
        return APIRequest().call(CommandsReview.call(review_id))
