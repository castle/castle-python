from castle.command import Command
from castle.exceptions import InvalidParametersError


class CommandsReview(object):
    def __init__(self, context):
        pass

    def build(self, review_id):
        if review_id is None or review_id == '':
            raise InvalidParametersError

        return Command(
            method='get',
            endpoint="reviews/{review_id}".format(review_id=review_id),
            data=None
        )
