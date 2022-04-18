import abc
import typing as t


class Source(metaclass=abc.ABCMeta):
    """
    A source of values to be tapped by configurations.

    **Abstract class.** Cannot be instantiated. Should be inherited from other source classes.

    Other packages can add more sources directly to the :mod:`cfig.sources` namespace package.
    """

    @abc.abstractmethod
    def get(self, key: str) -> t.Optional[str]:
        """
        Get the value with the given key from the source.
        """


__all__ = (
    "Source",
)
