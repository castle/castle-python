from castle.command import Command
from castle.validators.present import ValidatorsPresent


class CommandsReview(object):

    @staticmethod
    def build(review_id):
        ValidatorsPresent.call({'review_id': review_id}, 'review_id')

        return Command(
            method='get',
            path="reviews/{review_id}".format(review_id=review_id),
            data=None
        )
