"""
This module contains the definition of an example :class:`~cfig.config.Configuration` using :mod:`cfig`.
"""

# Import the cfig module, so it may be used in the file
import cfig
# Alias the typing module as t, so it can be used faster
import typing as t

# Create a new configuration using the default sources:
# - environment variables: EXAMPLE_VALUE
# - contents of the files specified in environment variables whose keys are suffixed by _FILE: EXAMPLE_VALUE_FILE
config = cfig.Configuration()


# Create a new proxy for a required configuration value
# It will behave in almost the same way as the object it is proxying
# The main differences are that:
# - "is" comparisions won't work: <Proxy None> is not None
# - some additional magic methods will be available, but you don't need to bother with them
@config.required()
def EXAMPLE_STRING(val: str) -> str:
    # The proxy is a function whose name will be used as key to access its value
    # Since this function is named EXAMPLE_STRING, and we are using the default sources, it will try to access in order:
    # - the EXAMPLE_STRING environment variable
    # - the file at the path specified in the EXAMPLE_STRING_FILE environment variable

    # The docstring of the function will be used to inform the user of what should be in this configuration option.
    """
    An example string: since this is an example, you can enter anything here, as it won't be used!
    It will have to be *something*, though.
    """

    # The code of the function will be used to process the "raw" value obtained from the sources
    # Since we do not want to alter the obtained value any further, we'll just return it
    return val


# Since the EXAMPLE_STRING proxy was defined as required, it will raise an error if no value is found at any source.
# Optional proxies exist, though!
@config.optional()
def EXAMPLE_NUMBER(val: t.Optional[str]) -> int:
    """
    An example number: again, since this is an example, it will not matter what value you will set it to.
    If you do not set it to anything, it will default to 0.
    """

    # Let's default to 0 in case the user doesn't pass any value
    if val is None:
        return 0

    # Otherwise, let's try to parse the value as an int
    try:
        return int(val)
    # It's possible that the user entered an invalid number, though, so let's handle that case
    except ValueError:
        # User errors are be handled explicitly so that the user knows it's not the programmer's fault
        raise cfig.InvalidValueError("Not an int.")


# And that's it!
# Let's make some more proxies as examples with no comments inbetween
# So you can have an easier idea of how cfig configs are made


@config.required()
def TELEGRAM_BOT_TOKEN(val: t.Optional[str]) -> str:
    """
    The token of the Telegram bot to login as.
    Obtain one at https://t.me/BotFather !
    """

    try:
        _id, _proper_token = val.split(":", 1)
    except ValueError:
        raise cfig.InvalidValueError("Not a Telegram bot token.")

    return val


@config.required()
def DISCORD_CLIENT_SECRET(val: t.Optional[str]) -> str:
    """
    The OAuth2 client secret of the Discord application to use.
    Obtain one at https://discord.com/developers/applications !
    """

    return val


# Proxies are lazily evaluated and executed only once, so you may use them to perform slower synchronous tasks
# For example, connecting to a database!
# They may be used even in global contexts such as in Flask or FastAPI apps without compromising their importability!


# Let's make a fake create_engine function so that I don't have to add sqlalchemy to cfig's dependencies
def create_engine(uri):
    ...


# Since the user inputs an URI, while we are creating a database
# We might want to use separate names for the "user-side" and the "programmer-side"
# We can specify the "user-side" name in the decorator
# And we can additionally specify the docstring
@config.required(key="DATABASE_URI", doc="The URI of the database to use.")
def DATABASE_ENGINE(val: str):
    return create_engine(uri=val)


# Finally, let's configure the config CLI
# Let's run the CLI only if this specific script is explicitly run
if __name__ == "__main__":
    # Then, pass the control to click
    # Argv will be automatically read and handled
    config.cli()
    # Please note that this will raise an error if the "cli" extra is not installed!
