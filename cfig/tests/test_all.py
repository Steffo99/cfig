import pytest
import cfig
import os
import lazy_object_proxy


class TestConfig:
    def test_creation(self):
        self.config = cfig.Configuration()

        assert isinstance(self.config, cfig.Configuration)
        assert self.config.sources == cfig.Configuration.DEFAULT_SOURCES

    def test_required(self):
        @self.config.required()
        def FIRST_NUMBER(val: str) -> int:
            """The first number to sum."""
            return int(val)

        assert isinstance(FIRST_NUMBER, lazy_object_proxy.Proxy)
        assert callable(FIRST_NUMBER.__factory__)
        assert not FIRST_NUMBER.__resolved__

        assert self.config.items["FIRST_NUMBER"] is FIRST_NUMBER
        assert self.config.docs["FIRST_NUMBER"] == """The first number to sum."""

        self.FIRST_NUMBER = FIRST_NUMBER

    def test_optional(self):
        @self.config.optional()
        def SECOND_NUMBER(val: str) -> int:
            """The second number to sum."""
            return int(val)

        assert isinstance(SECOND_NUMBER, lazy_object_proxy.Proxy)
        assert callable(SECOND_NUMBER.__factory__)
        assert not SECOND_NUMBER.__resolved__

        assert self.config.items["SECOND_NUMBER"] is SECOND_NUMBER
        assert self.config.docs["SECOND_NUMBER"] == """The second number to sum."""

        self.SECOND_NUMBER = SECOND_NUMBER

    def test_fetch_missing(self, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert not os.environ.get("FIRST_NUMBER")
        assert not os.environ.get("SECOND_NUMBER")

        with pytest.raises(cfig.MissingValueError):
            self.config.fetch_all()

    def test_fetch_required(self, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert not os.environ.get("SECOND_NUMBER")

        self.config.fetch_all()

        # noinspection PyUnresolvedReferences
        assert self.FIRST_NUMBER.__resolved__
        assert self.FIRST_NUMBER == 1
        # noinspection PyUnresolvedReferences
        assert self.SECOND_NUMBER.__resolved__
        assert self.SECOND_NUMBER == None
        assert self.SECOND_NUMBER is not None

    def test_fetch_optional(self, monkeypatch):
        monkeypatch.setenv("FIRST_NUMBER", "1")
        monkeypatch.setenv("SECOND_NUMBER", "2")

        assert os.environ.get("FIRST_NUMBER") == "1"
        assert os.environ.get("FIRST_NUMBER") == "2"

        self.config.fetch_all()

        # noinspection PyUnresolvedReferences
        assert self.FIRST_NUMBER.__resolved__
        assert self.FIRST_NUMBER == 1
        # noinspection PyUnresolvedReferences
        assert self.SECOND_NUMBER.__resolved__
        assert self.SECOND_NUMBER == 2
