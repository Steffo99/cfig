"""
Sample configuration module using :mod:`cfig`.
"""


import cfig
import typing


config = cfig.Configuration()


@config.required()
def MY_FAVOURITE_STRING(val: str) -> str:
    """
    Your favourite string!
    """
    return val


@config.optional()
def MY_OPTIONAL_STRING(val: typing.Optional[str]) -> str:
    """
    Your favourite string, but optional!
    """
    return val or ""


@config.required()
def MY_REQUIRED_INT(val: str) -> int:
    """
    Your favourite integer!
    """
    try:
        return int(val)
    except ValueError:
        raise cfig.InvalidValueError("Not an int.")


@config.required()
def MY_FAVOURITE_EVEN_INT(val: str) -> int:
    """
    Your favourite even number!
    """
    try:
        n = int(val)
    except ValueError:
        raise cfig.InvalidValueError("Not an int.")
    if n % 2:
        raise cfig.InvalidValueError("Not an even int.")
    return n


@config.required(key="KEY_NAME")
def VAR_NAME(val: str) -> str:
    """
    This config value looks for a key in the configuration sources but is available at a different key to the programmer.
    """
    return val


if __name__ == "__main__":
    config.cli()
