import typing as t
import abc
import os


class Source(metaclass=abc.ABCMeta):
    """
    A source of values to be tapped by configurations.
    """

    @abc.abstractmethod
    def get(self, key: str) -> t.Optional[str]:
        raise NotImplementedError()


class EnvironmentSource(Source):
    """
    A source which gets values from environment variables.
    """

    def __init__(self, *, prefix: str = "", suffix: str = "", environment=os.environ):
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

        self.environment = environment
        """
        The environment to retrieve variable values from.
        
        Defaults to :data:`os.environ`. 
        """

    def _process_key(self, key: str) -> str:
        return f"{self.prefix}{key}{self.suffix}"

    def get(self, key: str) -> t.Optional[str]:
        key = self._process_key(key)
        return self.environment.get(key)


class EnvironmentFileSource(EnvironmentSource):
    """
    A source which gets values from files at paths specified in environment variables.
    """

    def __init__(self, *, prefix: str = "", suffix: str = "_FILE", environment=os.environ):
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
    "Source",
    "EnvironmentSource",
    "EnvironmentFileSource",
)
