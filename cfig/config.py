"""
This module defines the :class:`Configuration` class.
"""

import lazy_object_proxy
import typing as t
import logging
import collections
import textwrap
from . import errors
from . import customtyping as ct
from cfig.sources.base import Source
from cfig.sources.env import EnvironmentSource
from cfig.sources.envfile import EnvironmentFileSource

log = logging.getLogger(__name__)


class Configuration:
    """
    A collection of proxies with methods to easily define more.
    """

    DEFAULT_SOURCES: list[Source] = [
        EnvironmentSource(),
        EnvironmentFileSource(),
    ]
    """
    The sources used in :meth:`__init__` if no other source is specified.
    """

    class ProxyDict(collections.UserDict):
        """
        An extended :class:`dict` with methods to perform some actions on the contained proxies.
        """

        def resolve(self) -> dict[str, t.Any]:
            """
            Resolve all values of the proxies inside this dictionary.

            :raises .errors.BatchResolutionFailure: If it was not possible to resolve at least one value.
            :returns: A :class:`dict` containing all the resolved, unproxied, values.
            """

            errors_dict = {}
            result_dict = {}

            log.debug("Resolving and caching all proxied values...")
            for key, proxy in self.items():
                log.debug(f"Resolving: {proxy!r}")
                try:
                    value = proxy.__wrapped__
                except Exception as e:
                    errors_dict[key] = e
                else:
                    result_dict[key] = value

            if errors_dict:
                raise errors.BatchResolutionFailure(errors=errors_dict)

            return result_dict

        def resolve_failfast(self) -> dict[str, t.Any]:
            """
            Resolve all values of the proxies inside this dictionary, failing immediately if an error occurs during a resolution, and raising the error itself.

            :raises Exception: The error occurred during the resolution.
            :returns: A :class:`dict` containing all the resolved, unproxied, values.
            """

            result_dict = {}

            log.debug("Resolving and caching all proxied values in failfast mode...")
            for key, proxy in self.items():
                log.debug(f"Resolving: {proxy!r}")
                value = proxy.__wrapped__
                result_dict[key] = value

            return result_dict

        def unresolve(self) -> None:
            """
            Unresolve all values of the proxies inside this dictionary.
            """

            log.debug("Unresolving all cached values...")
            for item in self.values():
                log.debug(f"Unresolving: {item!r}")
                del item.__wrapped__

    def __init__(self, *, sources: t.Optional[list[Source]] = None):
        """
        Create a new :class:`Configuration`.
        """

        log.debug(f"Initializing a new {self.__class__.__qualname__} object...")

        self.sources: list[Source] = sources or self.DEFAULT_SOURCES
        """
        Collection of sources to use for values of this configuration.
        """

        self.proxies: Configuration.ProxyDict = Configuration.ProxyDict()
        """
        Dictionary mapping configuration keys belonging to this :class:`.Configuration` to the proxy caching their values.
        
        Typed with :class:`typing.Any` so that proxies can be typed as the object they cache.
        """

        self.docs: dict[str, str] = {}
        """
        Dictionary mapping configuration keys belonging to this :class:`.Configuration` to a description of what they should contain.
        """

        log.debug("Initialized successfully!")

    def optional(self, key: t.Optional[str] = None, doc: t.Optional[str] = None) -> ct.ProxyOptional:
        """
        Mark a function as a resolver for a required configuration value.

        It is a decorator factory, and therefore should be used like so::

            @config.optional()
            def MY_KEY(val: str) -> str:
                return val

        Key can be overridden manually with the ``key`` parameter.

        Docstring can be overridden manually with the ``doc`` parameter.
        """

        def _decorator(configurable: ct.ResolverOptional) -> ct.TYPE:
            nonlocal key
            nonlocal doc

            if not key:
                log.debug("Determining key...")
                key = self._find_resolver_key(configurable)
                log.debug(f"Key is: {key!r}")

            log.debug("Creating optional item...")
            item: ct.TYPE = self._create_proxy_optional(key, configurable)
            log.debug("Item created successfully!")

            log.debug("Registering item in the configuration...")
            self.register(key, item, doc if doc is not None else configurable.__doc__)
            log.debug("Registered successfully!")

            # Return the created item, so it will take the place of the decorated function
            return item

        return _decorator

    def required(self, key: t.Optional[str] = None, doc: t.Optional[str] = None) -> ct.ProxyRequired:
        """
        Mark a function as a resolver for a required configuration value.

        It is a decorator factory, and therefore should be used like so::

            @config.required()
            def MY_KEY(val: str) -> str:
                return val

        Key can be overridden manually with the ``key`` parameter.

        Docstring can be overridden manually with the ``doc`` parameter.
        """

        def _decorator(configurable: ct.ResolverRequired) -> ct.TYPE:
            nonlocal key
            nonlocal doc

            if not key:
                log.debug("Determining key...")
                key = self._find_resolver_key(configurable)
                log.debug(f"Key is: {key!r}")

            log.debug("Creating required item...")
            item: ct.TYPE = self._create_proxy_required(key, configurable)
            log.debug("Item created successfully!")

            log.debug("Registering item in the configuration...")
            self.register(key, item, doc if doc is not None else configurable.__doc__)
            log.debug("Registered successfully!")

            # Return the created item, so it will take the place of the decorated function
            return item

        return _decorator

    # noinspection PyMethodMayBeStatic
    def _find_resolver_key(self, resolver: ct.ResolverAny) -> str:
        """
        Find the key of a resolver by accessing its ``__name__``.

        :raises .errors.UnknownResolverNameError: If the key could not be determined, for example if the resolver had no ``__name__``.
        """

        try:
            return resolver.__name__
        except AttributeError:
            log.error(f"Could not determine key of: {resolver!r}")
            raise errors.UnknownResolverNameError()

    def _retrieve_value_optional(self, key: str) -> t.Optional[str]:
        """
        Try to retrieve a value from all :attr:`.sources` of this :class:`.Configuration`, returning :data:`None` if the value is not found anywhere.
        """

        for source in self.sources:
            log.debug(f"Trying to retrieve {key!r} from {source!r}...")
            if value := source.get(key):
                log.debug(f"Retrieved {key!r} from {source!r}: {value!r}")
                return value
        else:
            log.debug(f"No values found for {key!r}, returning None.")
            return None

    def _create_proxy_optional(self, key: str, resolver: ct.ResolverOptional) -> ct.TYPE:
        """
        Create, from a resolver, a proxy tolerating non-specified values.
        """

        @lazy_object_proxy.Proxy
        def _decorated():
            log.debug(f"Retrieving value with key: {key!r}")
            val = self._retrieve_value_optional(key)
            log.debug("Retrieved value successfully!")

            log.debug("Running user-defined configurable function...")
            val = resolver(val)

            return val

        return _decorated

    def _retrieve_value_required(self, key: str) -> str:
        """
        Try to retrieve a value from all :attr:`.sources` of this Configuration, raising :exc:`errors.MissingValueError` if the value is not found anywhere.

        :raises .errors.MissingValueError: If the value with the given key is not found in any source.
        """

        if value := self._retrieve_value_optional(key):
            return value
        else:
            raise errors.MissingValueError(key)

    def _create_proxy_required(self, key: str, resolver: ct.ResolverRequired) -> ct.TYPE:
        """
        Create, from a resolver, a proxy intolerant about non-specified values.
        """

        @lazy_object_proxy.Proxy
        def _decorated():
            log.debug(f"Retrieving value with key: {key!r}")
            val = self._retrieve_value_required(key)
            log.debug("Retrieved val successfully!")

            log.debug("Running user-defined configurable function...")
            val = resolver(val)

            return val

        return _decorated

    def register(self, key, proxy, doc):
        """
        Register a new proxy in this Configuration.

        :param key: The configuration key to register the proxy to.
        :param proxy: The proxy to register in :attr:`.proxies`.
        :param doc: The docstring to register in :attr:`.docs`.
        :raises .errors.DuplicateProxyNameError`: if the key already exists in either :attr:`.proxies` or :attr:`.docs`.
        """

        if key in self.proxies:
            raise errors.DuplicateProxyNameError(key)
        if key in self.docs:
            raise errors.DuplicateProxyNameError(key)

        log.debug(f"Registering proxy {proxy!r} in {key!r}")
        self.proxies[key] = proxy
        log.debug(f"Registering doc {doc!r} in {key!r}")
        self.docs[key] = doc

    def _click_root(self):
        """
        Generate the :mod:`click` root of this :class:`.Configuration`.
        """

        try:
            import click
        except ImportError:
            raise errors.MissingDependencyError(f"To use {self.__class__.__qualname__}.cli, the `cli` optional dependency is needed.")

        @click.command()
        def root():
            click.secho(f"===== Configuration =====", fg="bright_white", bold=True)
            click.secho()

            key_padding = max(map(lambda k: len(k), self.proxies.keys()))

            try:
                self.proxies.resolve()
            except errors.BatchResolutionFailure as fail:
                errors_dict = fail.errors
            else:
                errors_dict = {}

            for key, proxy in self.proxies.items():
                # Weird padding hack
                # noinspection PyStringFormat
                key_text = f"{{key:{key_padding}}}".format(key=key)

                if key in errors_dict:
                    error = errors_dict[key]
                    if isinstance(error, errors.MissingValueError):
                        click.secho(f"{key_text} → Required, but not set.", fg="red")
                    elif isinstance(error, errors.InvalidValueError):
                        click.secho(f"{key_text} → {' '.join(error.args)}", fg="red")
                    else:
                        click.secho(f"{key_text} → {error!r}", fg="white", bg="bright_red")
                else:
                    value = self.proxies[key]
                    click.secho(f"{key_text} = {value.__wrapped__!r}", fg="green")

                doc = self.docs[key]
                doc = textwrap.dedent(doc)
                doc = doc.strip("\n")
                doc = "\n".join(doc.split("\n")[:3])

                click.secho(f"{doc}", fg="white")
                click.secho()

            click.secho(f"===== End =====", fg="bright_white", bold=True)

        return root

    def cli(self):
        """
        Run the command-line interface.
        """

        self._click_root()()


__all__ = (
    "Configuration",
)
