"""
This module defines the :class:`.EnvironmentFileSource` :class:`~cfig.sources.base.Source`.
"""

import typing as t
from cfig.sources.env import EnvironmentSource


class EnvironmentFileSource(EnvironmentSource):
    """
    A source which gets values from files at paths specified in environment variables.

    Useful for example with Docker Secrets.
    """

    def __init__(self, *, prefix: str = "", suffix: str = "_FILE", environment=None):
        super().__init__(prefix=prefix, suffix=suffix, environment=environment)

    def get(self, key: str) -> t.Optional[str]:
        path = super().get(key)
        if path is None:
            return None
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return None


__all__ = (
    "EnvironmentFileSource",
)
