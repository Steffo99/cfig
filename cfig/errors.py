class CfigError(Exception):
    """
    Base class for all :mod:`cfig` errors.
    """


class DefinitionError(CfigError):
    """
    An error is present in the definition of a :class:`cfig.Configuration`.

    This is a developer-side error: the user has no way to solve it.
    """


class UnknownResolverNameError(DefinitionError):
    """
    It was not possible to get the name of the resolver.

    Perhaps a call to :func:`functools.wraps` is missing?
    """


class ProxyRegistrationError(DefinitionError):
    """
    An error occurred during the proxy registration step.
    """


class DuplicateProxyNameError(ProxyRegistrationError):
    """
    Another proxy with the same name is already registered.
    """


class ConfigurationError(CfigError):
    """
    An error is present in the configuration specified by the user.

    This is a user-side error: the developer of the application has no way to solve it.
    """


class MissingValueError(ConfigurationError):
    """
    A required configuration key has no value.
    """


class BatchResolutionFailure(BaseException):
    """
    A cumulative error which sums the errors occurred while resolving proxied configuration values.
    """

    def __init__(self, errors: dict[str, Exception]):
        self.errors: dict[str, Exception] = errors

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {len(self.errors)} errors>"


__all__ = (
    "DefinitionError",
    "UnknownResolverNameError",
    "ProxyRegistrationError",
    "DuplicateProxyNameError",
    "ConfigurationError",
    "MissingValueError",
    "BatchResolutionFailure",
)
