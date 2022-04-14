"""
This package provides a simple-to-use but featureful configuration manager for Python applications.

A goal is to allow easy integration of an application with multiple configuration standards, such as environment
variables, dotenv files, and Docker Secrets files.

Another goal is to provide informative error messages to the user who is configuring the application, so that they may
understand what they are doing wrong and fix it immediately.

The final goal is for the package to be fully typed, so that useful information can be received by the developer
programming the consumption the configuration files.

Ideally, the configuration file for an application should look like this:

.. code-block:: python

    # Import the cfig library
    import cfig

    # Create a "Configurable" object
    config = cfig.Configurable()

    # Use the object to wrap configurable values
    @config.value()
    # Value information is determined by parameters of a function
    # Name, parameters, docstring, and return annotation are used
    # The function name is unusually in SCREAMING_SNAKE_CASE
    def SECRET_KEY(val: str) -> str:
        "Secret string used to manage tokens."
        return val

    @config.value()
    def ALLOWED_USERS(val: str) -> int:
        "The maximum number of allowed users in the application."
        # Values can be altered to become more useful to the programmer
        # Errors are managed by cfig
        return int(val)

    @config.value()
    # If the val variable has an Optional annotation, cfig will mark that value as optional
    def ACCEPTED_TERMS_AND_CONDITIONS(val: Optional[str]) -> bool:
        "To accept T&C, set this to a non-blank string."
        return val is not None

    if __name__ == "__main__":
        # If the configuration file is executed as main, handle the call and display a user-friendly CLI interface.
        config()

Configured values can later be accessed by importing the configuration file:

.. code-block:: python

    # Import the previously defined file
    from . import myconfig

    # Function is executed once when the value is first accessed
    print(f"Maximum allowed users: {myconfig.ALLOWED_USERS}")

Configuration files of dependencies can be merged into the current

"""

# noinspection PyUnresolvedReferences
from .config import *
# noinspection PyUnresolvedReferences
from .sources import *
# noinspection PyUnresolvedReferences
from .errors import *
# noinspection PyUnresolvedReferences
from .customtyping import *
