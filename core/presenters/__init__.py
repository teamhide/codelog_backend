import abc
from flask import jsonify


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def transform(cls, response) -> jsonify:
        pass
