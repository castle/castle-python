import logging
import sys
import unittest
from unittest import mock


TEST_MODULES = [
    'castle.test.api_test',
    'castle.test.apis.request_test',
    'castle.test.apis.response_test',
    'castle.test.apis.session_test',
    'castle.test.client_test',
    'castle.test.client_id.extract_test',
    'castle.test.command_test',
    'castle.test.commands.authenticate_test',
    'castle.test.commands.identify_test',
    'castle.test.commands.impersonate_test',
    'castle.test.commands.review_test',
    'castle.test.commands.track_test',
    'castle.test.configuration_test',
    'castle.test.context.get_default_test',
    'castle.test.context.merge_test',
    'castle.test.context.sanitize_test',
    'castle.test.failover.prepare_response_test',
    'castle.test.headers.extract_test',
    'castle.test.headers.filter_test',
    'castle.test.headers.format_test',
    'castle.test.ip.extract_test',
    'castle.test.review_test',
    'castle.test.secure_mode_test',
    'castle.test.utils.clone_test',
    'castle.test.utils.merge_test',
    'castle.test.utils.timestamp_test',
    'castle.test.validators.not_supported_test',
    'castle.test.validators.present_test',
]

# pylint: disable=redefined-builtin


def all():
    logging.basicConfig(stream=sys.stderr)
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
