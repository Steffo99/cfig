import pytest
import cfig
import os
import lazy_object_proxy
import typing as t

try:
    import click
    import click.testing
except ImportError:
    click = None


class TestConfig:
    def test_creation(self):
        config = cfig.Configuration()

        assert isinstance(config, cfig.Configuration)
        assert config.sources == cfig.Configuration.DEFAULT_SOURCES

    @pytest.fixture(scope="function")
    def basic_config(self):
        yield cfig.Configuration()

    def test_registration_required(self, basic_config):
        @basic_config.required()
        def FIRST_NUMBER(val: str) -> int:
            """The first number to sum."""
            try:
                return int(val)
            except (ValueError, TypeError):
                raise cfig.InvalidValueError("Not an int.")

        assert isinstance(FIRST_NUMBER, lazy_object_proxy.Proxy)
        assert callable(FIRST_NUMBER.__factory__)
        assert not FIRST_NUMBER.__resolved__
        assert basic_config.proxies["FIRST_NUMBER"] is FIRST_NUMBER
        assert basic_config.docs["FIRST_NUMBER"] == """The first number to sum."""

    def test_registration_optional(self, basic_config):
        @basic_config.optional()
        def SECOND_NUMBER(val: t.Optional[str]) -> t.Optional[int]:
            """The second number to sum."""
            if val is None:
                return None
            try:
                return int(val)
            except (ValueError, TypeError):
                raise cfig.InvalidValueError("Not an int.")

        assert isinstance(SECOND_NUMBER, lazy_object_proxy.Proxy)
        assert callable(SECOND_NUMBER.__factory__)
        assert not SECOND_NUMBER.__resolved__
        assert basic_config.proxies["SECOND_NUMBER"] is SECOND_NUMBER
        assert basic_config.docs["SECOND_NUMBER"] == """The second number to sum."""

    @pytest.fixture(scope="function")
    def numbers_config(self, basic_config):
        @basic_config.required()
        def FIRST_NUMBER(val: str) -> int:
            """The first number to sum."""
            try:
                return int(val)
            except (ValueError, TypeError):
                raise cfig.InvalidValueError("Not an int.")

        @basic_config.optional()
        def SECOND_NUMBER(val: t.Optional[str]) -> t.Optional[int]:
            """The second number to sum."""
            if val is None:
                return None
            try:
                return int(val)
            except (ValueError, TypeError):
                raise cfig.InvalidValueError("Not an int.")

        yield basic_config

    def test_resolve_missing(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert not os.environ.get("FIRST_NUMBER")
        assert not os.environ.get("SECOND_NUMBER")

        with pytest.raises(cfig.BatchResolutionFailure) as ei:
            numbers_config.proxies.resolve()
            assert isinstance(ei.value.errors["FIRST_NUMBER"], cfig.MissingValueError)

    def test_resolve_ff_missing(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert not os.environ.get("FIRST_NUMBER")
        assert not os.environ.get("SECOND_NUMBER")

        with pytest.raises(cfig.MissingValueError):
            numbers_config.proxies.resolve_failfast()

    def test_resolve_invalid(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "a")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER", "a")
        assert not os.environ.get("SECOND_NUMBER")

        with pytest.raises(cfig.BatchResolutionFailure) as ei:
            numbers_config.proxies.resolve()
            assert isinstance(ei.value.errors["FIRST_NUMBER"], cfig.InvalidValueError)

    def test_resolve_ff_invalid(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "a")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER", "a")
        assert not os.environ.get("SECOND_NUMBER")

        with pytest.raises(cfig.InvalidValueError):
            numbers_config.proxies.resolve_failfast()

    def test_resolve_required(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert not os.environ.get("SECOND_NUMBER")

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        result_dict = numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == None
        assert second_number is not None

        assert result_dict["FIRST_NUMBER"] == 1
        assert result_dict["SECOND_NUMBER"] == None
        assert result_dict["SECOND_NUMBER"] is None

    def test_resolve_ff_required(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert not os.environ.get("SECOND_NUMBER")

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        result_dict = numbers_config.proxies.resolve_failfast()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == None
        assert second_number is not None

        assert result_dict["FIRST_NUMBER"] == 1
        assert result_dict["SECOND_NUMBER"] == None
        assert result_dict["SECOND_NUMBER"] is None

    def test_resolve_optional(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("SECOND_NUMBER") == "2"

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        result_dict = numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

        assert result_dict["FIRST_NUMBER"] == 1
        assert result_dict["SECOND_NUMBER"] == 2

    def test_resolve_ff_optional(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("SECOND_NUMBER") == "2"

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        result_dict = numbers_config.proxies.resolve_failfast()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

        assert result_dict["FIRST_NUMBER"] == 1
        assert result_dict["SECOND_NUMBER"] == 2

    def test_resolve_unresolve(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("SECOND_NUMBER") == "2"

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        result_dict = numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

        assert result_dict["FIRST_NUMBER"] == 1
        assert result_dict["SECOND_NUMBER"] == 2

        monkeypatch.setenv("FIRST_NUMBER", "3")
        monkeypatch.setenv("SECOND_NUMBER", "4")

        assert os.environ.get("FIRST_NUMBER") == "3"
        assert os.environ.get("SECOND_NUMBER") == "4"

        result_dict = numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

        assert result_dict["FIRST_NUMBER"] == 1
        assert result_dict["SECOND_NUMBER"] == 2

        numbers_config.proxies.unresolve()

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        result_dict = numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 3

        assert second_number.__resolved__
        assert second_number == 4

        assert result_dict["FIRST_NUMBER"] == 3
        assert result_dict["SECOND_NUMBER"] == 4

    @pytest.fixture(scope="function")
    def click_runner(self):
        yield click.testing.CliRunner()

    @pytest.mark.skipif(click is None, reason="the `cli` extra is not installed")
    def test_cli(self, numbers_config, monkeypatch, click_runner):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert not os.environ.get("SECOND_NUMBER")

        root = numbers_config._click_root()
        result = click_runner.invoke(root, [])

        assert result.exit_code == 0
        assert "FIRST_NUMBER" in result.output
        assert "SECOND_NUMBER" in result.output
