from typing import Optional, Union

from . import google, numpy, sphinx
from .base import BaseDocstring  # noqa


class Docstring(object):
    """A factory method for creating docstrings."""

    @staticmethod
    def from_google(root: str) -> BaseDocstring:
        return google.Docstring(root)

    @staticmethod
    def from_sphinx(root, config: str = None) -> BaseDocstring:
        return sphinx.Docstring(root)

    @staticmethod
    def from_numpy(root, config: str = None) -> BaseDocstring:
        return numpy.Docstring(root)
