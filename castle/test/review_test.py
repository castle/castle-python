import json
import responses

from castle.test import unittest
from castle.review import Review


class ReviewTestCase(unittest.TestCase):
    @responses.activate
    def test_retrieve(self):
        # pylint: disable=line-too-long
        response_text = "{\"id\":\"56b32fa0-880b-0135-74d6-00e650213316\",\"reviewed\":false,\"created_at\":\"2017-09-15T11:59:57.211Z\",\"user_id\":\"1\",\"context\":{\"ip\":\"8.8.8.8\",\"location\":{\"country_code\":\"US\",\"country\":\"United States\",\"region\":null,\"region_code\":null,\"city\":null,\"lat\":37.751,\"lon\":-97.822},\"user_agent\":{\"raw\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36\",\"browser\":\"Chrome\",\"version\":\"60.0.3112\",\"os\":\"Mac OS X 10.12.6\",\"mobile\":false,\"platform\":\"Mac OS X\",\"device\":\"Unknown\",\"family\":\"Chrome\"}}}"
        responses.add(
            responses.GET,
            'https://api.castle.io/v1/reviews/1234',
            body=response_text,
            status=200
        )
        review_id = '1234'
        self.assertEqual(Review.retrieve(review_id), json.loads(response_text))
