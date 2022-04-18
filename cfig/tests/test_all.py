import pytest
import cfig
import os
import lazy_object_proxy


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
            return int(val)

        assert isinstance(FIRST_NUMBER, lazy_object_proxy.Proxy)
        assert callable(FIRST_NUMBER.__factory__)
        assert not FIRST_NUMBER.__resolved__
        assert basic_config.proxies["FIRST_NUMBER"] is FIRST_NUMBER
        assert basic_config.docs["FIRST_NUMBER"] == """The first number to sum."""

    def test_registration_optional(self, basic_config):
        @basic_config.optional()
        def SECOND_NUMBER(val: str) -> int:
            """The second number to sum."""
            return int(val)

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
            return int(val)

        @basic_config.optional()
        def SECOND_NUMBER(val: str) -> int:
            """The second number to sum."""
            return int(val)

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

    def test_resolve_required(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert not os.environ.get("SECOND_NUMBER")

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == None
        assert second_number is not None

    def test_resolve_ff_required(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert not os.environ.get("SECOND_NUMBER")

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        numbers_config.proxies.resolve_failfast()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == None
        assert second_number is not None

    def test_resolve_optional(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("SECOND_NUMBER") == "2"

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

    def test_resolve_ff_optional(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("SECOND_NUMBER") == "2"

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        numbers_config.proxies.resolve_failfast()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

    def test_resolve_unresolve(self, numbers_config, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("SECOND_NUMBER") == "2"

        first_number = numbers_config.proxies["FIRST_NUMBER"]
        second_number = numbers_config.proxies["SECOND_NUMBER"]

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

        monkeypatch.setenv("FIRST_NUMBER", "3")
        monkeypatch.setenv("SECOND_NUMBER", "4")

        assert os.environ.get("FIRST_NUMBER") == "3"
        assert os.environ.get("SECOND_NUMBER") == "4"

        numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 1

        assert second_number.__resolved__
        assert second_number == 2

        numbers_config.proxies.unresolve()

        assert not first_number.__resolved__
        assert not second_number.__resolved__

        numbers_config.proxies.resolve()

        assert first_number.__resolved__
        assert first_number == 3

        assert second_number.__resolved__
        assert second_number == 4
