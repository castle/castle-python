from castle.command import Command
from castle.validators import ValidatorsPresent


class CommandsReview(object):

    def build(self, review_id):
        ValidatorsPresent.call({'review_id': review_id}, 'review_id')

        return Command(
            method='get',
            path="reviews/{review_id}".format(review_id=review_id),
            data=None
        )
