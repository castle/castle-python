import json

from castle.version import VERSION
from castle.system import System

__version__ = VERSION

class Headers(object):
    def defaults(self):
        {
            'Content-Type': 'application/json',
            'User-Agent': "Castle/v1 PythonBindings/{__version__}"
        }

    def build(self, client_id, ip, castle_headers):
        self.headers = dict(defaults)
        self.headers.update(self.castle(client_id, ip, castle_headers))
        self.headers

    def castle(self, client_id, ip, castle_headers):
        {
	    'X-Castle-Client-Id': client_id,
	    'X-Castle-Ip': ip,
	    'X-Castle-Headers': castle_headers,
	    'X-Castle-Client-User-Agent': json.dumps(self.client_user_agent),
	    'X-Castle-Source': 'web'
        }


    def client_user_agent(self):
        {
            'bindings_version': __version__,
            'lang': 'python',
            'lang_version': System.python_version(),
            'platform': System.platform(),
            'publisher': 'castle',
            'uname': System.uname()
        }
