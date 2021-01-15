from castle.configuration import Configuration

class SingletonConfiguration(Configuration):

    instance = None

    def __new__(cls, *args, **kwargs):
        if not SingletonConfiguration.instance:
            SingletonConfiguration.instance = super().__new__(cls, *args, **kwargs)
        return SingletonConfiguration.instance
