from castle.api import Api
from castle.commands.review import CommandsReview


class Review(object):
    @staticmethod
    def retrieve(review_id):
        return Api().call(CommandsReview.build(review_id))
