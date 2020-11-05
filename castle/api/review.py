from castle.api import Api
from castle.commands.review import CommandsReview


class APIReview(object):
    @staticmethod
    def retrieve(review_id):
        return Api().call(CommandsReview.build(review_id))
