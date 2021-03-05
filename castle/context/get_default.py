from castle.version import VERSION

__version__ = VERSION


class ContextGetDefault(object):

    @staticmethod
    def call():
        context = dict({
            'active': True,
            'library': {
                'name': 'castle-python',
                'version': __version__
            }
        })

        return context
