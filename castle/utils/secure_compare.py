import sys


class UtilsSecureCompare(object):

    @staticmethod
    def call(str_a, str_b):
        """
        Compare two strings securely

        :param str_a: First string to be compared
        :param str_b: Second string to be compared
        """
        if not sys.getsizeof(str_a) == sys.getsizeof(str_b):
            return False

        comp_a = [int(str_a_char) for str_a_char in bytes(str_a.encode('utf-8'))]

        res = 0
        for str_b_char in bytes(str_b.encode('utf-8')):
            res |= str_b_char ^ comp_a.pop(0)

        return res == 0
