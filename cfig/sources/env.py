"""
This module defines the :class:`.EnvironmentSource` :class:`~cfig.sources.base.Source`.
"""

import os
import typing as t
from cfig.sources.base import Source


class EnvironmentSource(Source):
    """
    A source which gets values from environment variables.
    """

    def __init__(self, *, prefix: str = "", suffix: str = "", environment=None):
        self.prefix: str = prefix
        """
        The prefix to be prepended to all environment variable names.
        
        For example, ``PROD_`` for production environment variables. 
        """

        self.suffix: str = suffix
        """
        The suffix to be appended to all environment variable names.
        
        For example, ``_VAL`` for raw values.
        """

        self.environment = environment if environment is not None else os.environ
        """
        The environment to retrieve variable values from.
        
        Defaults to :data:`os.environ`. 
        """

    def _process_key(self, key: str) -> str:
        return f"{self.prefix}{key}{self.suffix}"

    def get(self, key: str) -> t.Optional[str]:
        key = self._process_key(key)
        return self.environment.get(key)
