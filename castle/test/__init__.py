import logging
import sys
import unittest
from unittest import mock


TEST_MODULES = [
    'castle.test.apis.request_test',
    'castle.test.apis.response_test',
    'castle.test.apis.session_test',
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
    'castle.test.review_test',
    'castle.test.secure_mode_test',
    'castle.test.validators.not_supported_test',
    'castle.test.validators.present_test',
    'castle.test.utils_test',
    'castle.test.utils2.merge_test',
    'castle.test.utils2.clone_test',
]

# pylint: disable=redefined-builtin


def all():
    logging.basicConfig(stream=sys.stderr)
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
