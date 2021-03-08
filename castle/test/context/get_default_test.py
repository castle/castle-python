from castle.test import unittest, mock

from castle.version import VERSION as __version__
from castle.context.get_default import ContextGetDefault


class ContextGetDefaultTestCase(unittest.TestCase):

    def test_default_context(self):
        context = ContextGetDefault.call()
        self.assertEqual(context['active'], True)
        self.assertDictEqual(
            context['library'],
            {'name': 'castle-python', 'version': __version__}
        )
