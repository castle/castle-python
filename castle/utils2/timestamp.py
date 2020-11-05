from datetime import datetime


class UtilsTimestamp(object):

    @staticmethod
    def call():
        """Return an ISO8601 timestamp representing the current datetime in UTC."""
        return datetime.utcnow().isoformat()
