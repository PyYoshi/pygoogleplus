# -*- coding:utf-8 -*-

from pygplus.errors import PyGplusErrors
from pygplus.model import ModelFactory

class ModelParser(object):
    """ description """

    def __init__(self):
        self.model_factory = ModelFactory

    def parse_error(self):
        """
        description
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        pass

    def parser(self,method,model_type,data):
        """
        description
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        """
        model = getattr(self.model_factory,model_type)
        result = model.parse(method, data)
        return result
    