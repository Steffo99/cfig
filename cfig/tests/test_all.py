import pytest
import cfig


def test_config(monkeypatch):
    config = cfig.Configuration()

    @config.required()
    def FIRST_NUMBER(val: str) -> int:
        """The first number to sum."""
        return int(val)

    @config.optional()
    def SECOND_NUMBER(val: str) -> int:
        """The second number to sum."""
        return int(val)

    # Assert the two configuration items have been registered
    assert "FIRST_NUMBER" in config.items
    assert "FIRST_NUMBER" in config.docs
    assert "SECOND_NUMBER" in config.items
    assert "SECOND_NUMBER" in config.docs

    # Assert docstrings are accessible even if the two items aren't
    assert config.docs["FIRST_NUMBER"] == """The first number to sum."""
    assert config.docs["SECOND_NUMBER"] == """The second number to sum."""

    # Assert that an error is raised if items are fetched without any value set
    with pytest.raises(cfig.MissingValueError):
        config.fetch_all()

    # Setup the environment
    monkeypatch.setenv("FIRST_NUMBER", "1")

    # Assert that no error is raised with all required values set
    config.fetch_all()

    # Assert the two variables have the correct values
    assert FIRST_NUMBER == 1
    assert SECOND_NUMBER == None

    # Please note that SECOND_NUMBER is not the same instance as None, as it is a lazy object proxy!
    assert SECOND_NUMBER is not None
