import pkgutil
import logging
import sys


# The unittest module got a significant overhaul
# in 2.7, so if we're in 2.6 we can use the backported
# version unittest2.
if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest


# Python 3 includes mocking, while 2 requires an extra module.
if sys.version_info[0] == 2:
    import mock
else:
    from unittest import mock

TEST_MODULES = [
    'castle.test.configuration_test',
    'castle.test.context.default_test',
    'castle.test.extractors.client_id_test',
    'castle.test.extractors.headers_test',
    'castle.test.extractors.ip_test',
    'castle.test.headers_formatter_test'
]

def all():
    logging.basicConfig(stream=sys.stderr)
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
