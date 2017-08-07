from __future__ import division
from datetime import datetime
import time
import warnings
import pdb

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

try:
    from datetime import timezone
    USE_PY3_TIMESTAMPS = True
except ImportError:
    USE_PY3_TIMESTAMPS = False

warnings.simplefilter("default")

class CastleIOException(Exception):
    pass


class CastleIO(object):
    def __init__(self, api_key=None, host=None, port=None, url_prefix=None, retries=3, timeout=10, backoff_factor=0.02):
        self.api_key = api_key
        self.host = host or 'api.castle.io'
        self.port = port or 443
        self.url_prefix = url_prefix or '/v1'
        self.retries = retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor

        self.setup_base_url()
        self.setup_connection()

    def setup_base_url(self):
        template = 'http://{host}:{port}/{prefix}'
        if self.port == 443:
            template = 'https://{host}/{prefix}'

        if '://' in self.host:
            self.host = self.host.split('://')[1]

        self.base_url = template.format(
            host=self.host.strip('/'),
            port=self.port,
            prefix=self.url_prefix.strip('/'))

    def setup_connection(self):
        self.http = Session()
        # Retry request a number of times before raising an exception
        # also define backoff_factor to delay each retry
        self.http.mount('https://', HTTPAdapter(max_retries=Retry(
            total=self.retries, backoff_factor=self.backoff_factor)))
        self.http.auth = ('', self.api_key)

    def get_query_string(self, action):
        '''Generates an API path'''
        return '{base}/{action}'.format(base=self.base_url, action=action)

    def send_request(self, method, url, data):
        '''Dispatches the request and returns a response'''

        try:
            response = self.http.request(method, url=url, json=self._sanitize(data), timeout=self.timeout)
        except Exception as e:
            # Raise exception alerting user that the system might be
            # experiencing an outage and refer them to system status page.
            message = '''Failed to receive valid reponse after {count} retries.
Check system status at http://status.customer.io.
Last caught exception -- {klass}: {message}
            '''.format(klass=type(e), message=e, count=self.retries)
            raise CastleIOException(message)

        result_status = response.status_code
        if result_status != 200:
            raise CastleIOException('%s: %s %s' % (result_status, url, data))
        return response.text

    def authenticate(self, name, user_id, **kwargs):
        '''Authenticate a single user by their user id, and optionally add attributes'''
        url = self.get_query_string('authenticate')
        self.send_request('POST', url, { 'name': name, 'user_id': user_id })

    def _sanitize(self, data):
        for k, v in data.items():
            if isinstance(v, datetime):
                data[k] = self._datetime_to_timestamp(v)
        return data

    def _datetime_to_timestamp(self, dt):
        if USE_PY3_TIMESTAMPS:
            return int(dt.replace(tzinfo=timezone.utc).timestamp())
        else:
            return int(time.mktime(dt.timetuple()))
