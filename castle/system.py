import sys
import os

class System(object):
    def python_version(self):
        return sys.version

    def platform(self):
        return sys.platform

    def uname(self):
        return os.uname().version
