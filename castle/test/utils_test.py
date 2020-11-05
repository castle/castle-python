from datetime import datetime

from castle.test import mock, unittest
from castle.utils import timestamp


class TimestampTestCase(unittest.TestCase):

    @mock.patch('castle.utils.datetime')
    def test_it_should_use_iso_format(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(
            2018, 1, 2, 3, 4, 5, 678901)
        expected = '2018-01-02T03:04:05.678901'
        self.assertEqual(timestamp(), expected)
