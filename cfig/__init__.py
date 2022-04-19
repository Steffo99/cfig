"""
This package provides a simple but powerful configuration manager for Python applications.

A goal is to allow easy integration of an application with multiple configuration standards, such as environment
variables, dotenv files, and Docker Secrets files.

.. code-block:: python

    @config.required()
    def SECRET_KEY(val: str) -> str:
        "Secret string used to manage tokens."
        return val

Another goal is to provide informative error messages to the user who is configuring the application, so that they may
understand what they are doing wrong and fix it immediately.

.. code-block:: console

    $ python -m cfig.sample
    === Configuration ===

    SECRET_KEY    → Required, but not set.
    Secret string used to manage HTTP session tokens.

    HIDDEN_STRING = 'amogus'
    A string which may be provided to silently print a string to the console.


Example
=======

Ideally, a "config" module should be created, where the programmer defines the possible configuration options of their
application::

    # Import the cfig library
    import cfig

    # Create a "Configuration" object
    config = cfig.Configuration()

    # Define configurable values by wrapping functions with the config decorators
    # Function name is used by default as the key of the variable to read
    @config.required()
    def SECRET_KEY(val: str) -> str:
        "Secret string used to manage tokens."
        return val

    @config.required()
    def ALLOWED_USERS(val: str) -> int:
        "The maximum number of allowed users in the application."
        # Values can be processed inside these functions
        return int(val)

    @config.optional()
    def ACCEPTED_TERMS_AND_CONDITIONS(val: Optional[str]) -> bool:
        "To accept T&C, set this to a non-blank string."
        return val is not None

    # If heavy processing is done inside the function, it may be useful to define the configuration key manually
    @config.required(key="DATABASE_URI", doc="The URI of the database to be used.")
    def DATABASE_ENGINE(val: str):
        return sqlalchemy.create_engine(val)

    if __name__ == "__main__":
        # If the configuration file is executed as main, handle the call and display a user-friendly CLI interface.
        config.cli()

Values can later be accessed by the program by importing the configuration file:

.. code-block:: python

    # Import the previously defined file
    from . import myconfig

    # Function is executed once when the value is first accessed
    print(f"Maximum allowed users: {myconfig.ALLOWED_USERS}")

    # Advanced objects can be loaded directly from the config
    Session = sessionmaker(bind=myconfig.DATABASE_ENGINE)


Terminology
===========

In this documentation, the following terms are used:

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

"""

# noinspection PyUnresolvedReferences
from .config import *
# noinspection PyUnresolvedReferences
from .errors import *
# noinspection PyUnresolvedReferences
from .customtyping import *
