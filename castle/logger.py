from castle.configuration import configuration


class Logger(object):

    @staticmethod
    def call(message, data="", config=configuration):
        """
        Log the message with optionally data using preconfigured logger

        :param message: The base logger message.
        :param data: Additional data passed optionally.
        :param config: Castle configuration.
        """
        logger = config.logger

        if not logger:
            return None

        msg = "[CASTLE] {} {}".format(message, data).strip()
        return logger.info(msg)
