from datetime import datetime


def timestamp():
    """Return an ISO8601 timestamp representing the current datetime in UTC."""
    return datetime.utcnow().isoformat()
