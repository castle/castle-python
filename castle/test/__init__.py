import logging
import sys


# The unittest module got a significant overhaul
# in 2.7, so if we're in 2.6 we can use the backported
# version unittest2.
if sys.version_info[:2] == (2, 6):
    # pylint: disable=import-error
    import unittest2 as unittest
else:
    import unittest


# Python 3 includes mocking, while 2 requires an extra module.
if sys.version_info[0] == 2:
    # pylint: disable=import-error
    import mock
else:
    from unittest import mock

if sys.version_info[:2] == (2, 6):
    import subprocess
    subprocess.call(["sed", "-i", "-e",  's/import _io/import io as _io/g', "/home/travis/build/castle/castle-python/.eggs/responses-0.6.2-py2.6.egg/responses.py"])

TEST_MODULES = [
    'castle.test.api_test',
    'castle.test.client_test',
    'castle.test.configuration_test',
    'castle.test.context.default_test',
    'castle.test.context.merger_test',
    'castle.test.context.sanitizer_test',
    'castle.test.command_test',
    'castle.test.commands.authenticate_test',
    'castle.test.commands.identify_test',
    'castle.test.commands.impersonate_test',
    'castle.test.commands.track_test',
    'castle.test.commands.review_test',
    'castle.test.extractors.client_id_test',
    'castle.test.extractors.headers_test',
    'castle.test.extractors.ip_test',
    'castle.test.failover_response_test',
    'castle.test.headers_formatter_test',
    'castle.test.request_test',
    'castle.test.response_test',
    'castle.test.review_test',
    'castle.test.secure_mode_test',
    'castle.test.session_test',
    'castle.test.validators.not_supported_test',
    'castle.test.validators.present_test',
    'castle.test.utils_test'
]

# pylint: disable=redefined-builtin


def all():
    logging.basicConfig(stream=sys.stderr)
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
