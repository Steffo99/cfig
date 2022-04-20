"""
This module contains an example of how to use the values defined in a cfig definition module.
"""

from .definition import EXAMPLE_STRING, EXAMPLE_NUMBER, DATABASE_ENGINE


if __name__ == "__main__":
    print(f"Hey! The example string you entered was {EXAMPLE_STRING}!")

    # IDEA seems to be a bit confused here
    # noinspection PyTypeChecker
    print(f"And the square of the example number was {EXAMPLE_NUMBER ** 2}!")

    print(f"We should do something with that {DATABASE_ENGINE} we created...")
