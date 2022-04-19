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
    Your favourite string, including the empty one!
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


if __name__ == "__main__":
    config.cli()
