# -*- coding:utf-8 -*-

class PyGplusErrors(Exception):
    """ description """

    def __init__(self,reason, response=None):
        """
        description
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        self.reason = reason
        self.response = response

    def __str__(self):
        return self.reason + "\n" + self.response

    def get_response(self):
        return self.response