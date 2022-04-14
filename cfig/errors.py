class DefinitionError(Exception):
    """
    An error is present in the definition of a :class:`cfig.Configurable` object.
    """


class UnknownKeyError(DefinitionError):
    """
    It was not possible to get the name of the wrapped function.

    Perhaps a call to :func:`functools.wraps` is missing?
    """


class RegistrationError(DefinitionError):
    """
    An error occurred during the proxy registration step.
    """


class DuplicateError(RegistrationError):
    """
    Another proxy with the same name is already registered.
    """


class ConfigurationError(Exception):
    """
    An error is present in the configuration specified by the user.
    """


class MissingValueError(ConfigurationError):
    """
    A required configuration key has no value.
    """


__all__ = (
    "DefinitionError",
    "UnknownKeyError",
    "RegistrationError",
    "DuplicateError",
    "ConfigurationError",
    "MissingValueError",
)
