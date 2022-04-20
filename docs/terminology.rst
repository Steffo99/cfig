###########
Terminology
###########

In this documentation, the following terms are used:

.. glossary::

    Key
        The name of a configuration value, usually in SCREAMING_SNAKE_CASE.
        For example, ``PATH``, the name of the environment variable.

    Value
        A single non-processed configuration value in :class:`str` form.
        For example, the raw string value of an environment variable.

    Source
        A possible origin of configuration values, such as the environment, or a file.

    Proxy
        An object used to lazily and transparently resolve and cache values.
        After resolving a value, it behaves in almost completely the same way as the object it cached.

    Resolver
        A function taking in input a value originating from a source, and emitting in output its processed representation.
        For example, a resolver may be the :class:`int` class, which converts the value into an integer.

    Configuration
        A collection of proxies.
