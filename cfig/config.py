"""
This module defines the :class:`Configuration` class.

The used terminology is:

Key
    The base name of a configuration value.
    For example, the name of an environment variable.

Value
    A single non-processed configuration value in :class:`str` form.
    For example, the raw string value of an environment variable.

Item
    A single processed value in any form.
    Internally, this is a :class:`lazy_object_proxy.Proxy`: an object whose value is not retrieved until it is accessed.

Configurable
    A specially decorated function that processes a value before it is turned into an item.

Configuration
    A group of items.
"""

import os
import lazy_object_proxy
import typing as t
import logging
from . import errors
from . import customtyping as ct
from . import sources as s

log = logging.getLogger(__name__)


class Configuration:
    """
    A group of configurable items.
    """

    DEFAULT_SOURCES = [
        s.EnvironmentSource(),
        s.EnvironmentFileSource(),
    ]

    def __init__(self, *, sources: t.Optional[t.Collection[s.Source]] = None):
        log.debug(f"Initializing a new {self.__class__.__qualname__} object...")

        self.sources: t.Collection[s.Source] = sources or self.DEFAULT_SOURCES
        """
        Collection of all places from where values should be retrieved from.
        """

        self.items: dict[str, t.Any] = {}
        """
        :class:`dict` mapping all keys registered to this object to their respective items.
        """

        self.docs: dict[str, str] = {}
        """
        :class:`dict` mapping all keys registered to this object to the description of what they should contain.
        """

        log.debug("Initialized successfully!")

    # noinspection PyMethodMayBeStatic
    def _determine_configurable_key(self, f: ct.Configurable) -> str:
        """
        Determine the key of a configurable.
        """

        try:
            return f.__name__
        except AttributeError:
            log.error(f"Could not determine key of: {f!r}")
            raise errors.UnknownKeyError()

    def required(self) -> t.Callable[[ct.ConfigurableRequired], ct.TYPE]:
        """
        Create the decorator to convert the decorated function into a required configurable.
        """

        def _decorator(configurable: ct.ConfigurableRequired) -> ct.TYPE:
            log.debug("Determining key...")
            key: str = self._determine_configurable_key(configurable)
            log.debug(f"Key is: {key!r}")

            log.debug("Creating required item...")
            item: ct.TYPE = self._create_item_required(key, configurable)
            log.debug("Item created successfully!")

            log.debug("Registering item in the configuration...")
            self._register_item(key, item, configurable.__doc__)
            log.debug("Registered successfully!")

            # Return the created item so it will take the place of the decorated function
            return item

        return _decorator

    def optional(self) -> t.Callable[[ct.ConfigurableOptional], ct.TYPE]:
        """
        Create the decorator to convert the decorated function into a required configurable.
        """

        def _decorator(configurable: ct.ConfigurableOptional) -> ct.TYPE:
            log.debug("Determining key...")
            key: str = self._determine_configurable_key(configurable)
            log.debug(f"Key is: {key!r}")

            log.debug("Creating optional item...")
            item: ct.TYPE = self._create_item_optional(key, configurable)
            log.debug("Item created successfully!")

            log.debug("Registering item in the configuration...")
            self._register_item(key, item, configurable.__doc__)
            log.debug("Registered successfully!")

            # Return the created item so it will take the place of the decorated function
            return item

        return _decorator

    def _create_item_optional(self, key: str, f: ct.ConfigurableOptional) -> lazy_object_proxy.Proxy:
        """
        Create a new optional item.
        """

        @lazy_object_proxy.Proxy
        def _decorated():
            log.debug(f"Retrieving value with key: {key!r}")
            val = self._retrieve_value_optional(key)
            log.debug("Retrieved value successfully!")

            if val is None:
                log.debug(f"Not running user-defined configurable function since value is {val!r}.")
            else:
                log.debug("Running user-defined configurable function...")
                val = f(val)

            log.info(f"{key} = {val!r}")
            return val

        return _decorated

    def _create_item_required(self, key: str, f: ct.ConfigurableRequired) -> lazy_object_proxy.Proxy:
        """
        Create a new required item.
        """

        @lazy_object_proxy.Proxy
        def _decorated():
            log.debug(f"Retrieving value with key: {key!r}")
            val = self._retrieve_value_required(key)
            log.debug("Retrieved val successfully!")

            log.debug("Running user-defined configurable function...")
            val = f(val)
            log.info(f"{key} = {val!r}")

            return val

        return _decorated

    def _retrieve_value_optional(self, key: str) -> t.Optional[str]:
        """
        Try to retrieve a value from all :attr:`.sources` of this Configuration.
        """

        for source in self.sources:
            log.debug(f"Trying to retrieve {key!r} from {source!r}...")
            if value := source.get(key):
                log.debug(f"Retrieved {key!r} from {source!r}: {value!r}")
                return value
        else:
            log.debug(f"No values found for {key!r}, returning None.")
            return None

    def _retrieve_value_required(self, key: str) -> str:
        """
        Retrieve a new value from all supported configuration schemes in :class:`str` form.
        """

        if value := self._retrieve_value_optional(key):
            return value
        else:
            raise errors.MissingValueError(key)

    def _register_item(self, key, item, doc):
        """
        Register an item in this Configuration.
        """

        if key in self.items:
            raise errors.DuplicateError(key)
        if key in self.docs:
            raise errors.DuplicateError(key)

        self.items[key] = item
        self.docs[key] = doc

    def fetch_all(self):
        log.debug("Fetching now all configuration items...")
        for value in self.items.values():
            _ = value.__wrapped__


__all__ = (
    "Configuration",
)
