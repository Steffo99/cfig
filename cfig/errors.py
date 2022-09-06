"""
This module contains all possible exceptions occurring related to :mod:`cfig`.
"""


class CfigError(Exception):
    """
    Base class for all :mod:`cfig` errors.
    """


class DeveloperError(CfigError):
    """
    A developer-side error: the user has no way to solve it.
    """


class DefinitionError(DeveloperError):
    """
    An error is present in the definition of a :class:`cfig.Configuration`.
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


class UserError(CfigError):
    """
    A user-side error: the developer of the application has no way to fix it.
    """


class ConfigurationError(UserError):
    """
    An error is present in the configuration specified by the user.
    """


class MissingValueError(ConfigurationError):
    """
    A required configuration key has no value.
    """


class InvalidValueError(ConfigurationError):
    """
    A configuration key has an invalid value.

    This error should be raised by the developer in resolvers if the developer knows that a invalid value has been passed, for example::

        @config.required()
        def INTEGER(val):
            try:
                return int(val)
            except ValueError:
                raise InvalidValueError("Not an int.")

    It is not raised automatically, as certain errors might be caused by a mistake in the programming of the resolver.
    """


class BatchResolutionFailure(BaseException):
    """
    A cumulative error which sums the errors occurred while resolving proxied configuration values.

    It inherits from :class:`BaseException` to be distinguishable from regular :class:`Exception`s occouring inside the resolvers.

    It uses some formatting tricks to display the missing keys in the configuration error message:

    .. code-block:: console

        $ python -m cfig.sample.usage
        Traceback (most recent call last):
          ...
          File "./cfig/sample/usage.py", line 7, in <module>
            config.proxies.resolve()
          File "./cfig/config.py", line 59, in resolve
            raise errors.BatchResolutionFailure(errors=errors_dict)
        cfig.errors.BatchResolutionFailure: 4 errors occurred during the resolution of the config:
        * EXAMPLE_NUMBER        → InvalidValueError: Not an int.
        * TELEGRAM_BOT_TOKEN    → MissingValueError: TELEGRAM_BOT_TOKEN
        * DISCORD_CLIENT_SECRET → MissingValueError: DISCORD_CLIENT_SECRET
        * DATABASE_URI          → MissingValueError: DATABASE_URI
    """

    def __init__(self, errors: dict[str, Exception]):
        message = [f"{len(errors)} errors occurred during the resolution of the config:"]

        key_padding = max(map(lambda k: len(k), errors.keys()))

        for key, val in errors.items():
            # Weird padding hack, part 2
            # noinspection PyStringFormat
            key_text = f"{{key:{key_padding}}}".format(key=key)

            message.append(f"* {key_text} → {val.__class__.__qualname__}: {val}")

        super().__init__("\n".join(message))

        self.errors: dict[str, Exception] = errors

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {len(self.errors)} errors>"


class MissingDependencyError(CfigError):
    """
    An optional dependency has not been installed, but it is required by a called function.
    """


__all__ = (
    "CfigError",
    "DeveloperError",
    "DefinitionError",
    "UnknownResolverNameError",
    "ProxyRegistrationError",
    "DuplicateProxyNameError",
    "UserError",
    "ConfigurationError",
    "MissingValueError",
    "InvalidValueError",
    "BatchResolutionFailure",
    "MissingDependencyError",
)
